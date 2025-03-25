import os
import sys
import json
import warnings
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader
from utils.load_config import load_config
from utils.logger import logger

# Ensure import path for project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def load_data(json_file):
    """Load rows and metrics from JSON file."""
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"File not found: {json_file}. Ensure the path is correct.")
    
    with open(json_file, 'r') as f:
        data = json.load(f)

    return data.get('rows', []), data.get('metrics', {})


def create_accuracy_metrics_chart(metrics):
    """Create bar chart for accuracy metrics."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)

        metrics_df = pd.DataFrame({
            'Metric': [
                'Function Name Accuracy',
                'Plugin Name Accuracy',
                'Arguments Accuracy',
                'Overall Accuracy'
            ],
            'Value': [
                metrics['end_to_end_function_call.Function_name_accuracy'],
                metrics['end_to_end_function_call.Plugin_name_accuracy'],
                metrics['end_to_end_function_call.Arguments_accuracy'],
                metrics['end_to_end_function_call.Overall_accuracy']
            ]
        })

        fig = px.bar(
            metrics_df, x='Metric', y='Value',
            color='Metric',
            text=metrics_df['Value'].apply(lambda x: f'{int(x*100)}%')
        )

        fig.update_layout(
            yaxis_title='Accuracy',
            yaxis_tickformat=',.0%',
            yaxis_range=[0, 1],
            showlegend=False
        )

        return fig.to_html(full_html=False)


def create_function_distribution_chart(df):
    """Create pie chart for function name distribution."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)

        function_counts = df['inputs.predicted_function'].apply(
            lambda x: x[0]['function_name'] if x else None
        ).value_counts()

        fig = px.pie(values=function_counts.values, names=function_counts.index)
        return fig.to_html(full_html=False)


def create_plugin_distribution_chart(df):
    """Create pie chart for plugin name distribution."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)

        plugin_counts = df['inputs.predicted_function'].apply(
            lambda x: x[0]['plugin_name'] if x else None
        ).value_counts()

        fig = px.pie(values=plugin_counts.values, names=plugin_counts.index)
        return fig.to_html(full_html=False)


def create_plugin_overall_accuracy_chart(data):
    """Create bar chart for overall accuracy by plugin name."""
    plugin_metrics = {}
    for row in data:
        for func in row['inputs.expected_function']:
            plugin = func['plugin_name']
            plugin_metrics.setdefault(plugin, {'total': 0, 'correct': 0})
            plugin_metrics[plugin]['total'] += 1
            plugin_metrics[plugin]['correct'] += int(row['outputs.end_to_end_function_call.Overall_accuracy'])

    plugin_data = [
        {
            'name': name,
            'accuracy': (m['correct'] / m['total'] * 100),
            'total': m['total']
        } for name, m in plugin_metrics.items()
    ]
    plugin_data.sort(key=lambda x: x['accuracy'], reverse=True)

    def get_color(acc):
        if acc >= 80: return '#27ae60'
        elif acc >= 60: return '#f1c40f'
        elif acc >= 40: return '#e67e22'
        else: return '#e74c3c'

    fig = go.Figure([
        go.Bar(
            x=[d['name'] for d in plugin_data],
            y=[d['accuracy'] for d in plugin_data],
            text=[f"{d['accuracy']:.0f}%<br>({d['total']} calls)" for d in plugin_data],
            textposition='auto',
            marker_color=[get_color(d['accuracy']) for d in plugin_data],
            hovertemplate="<b>%{x}</b><br>Accuracy: %{y:.1f}%<extra></extra>"
        )
    ])

    fig.update_layout(
        xaxis_title='Plugin Name',
        yaxis=dict(
            title='Overall Accuracy (%)',
            range=[0, 100],
            tickformat=',.0%',
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        showlegend=False,
        bargap=0.3
    )

    return fig.to_html(full_html=False)


def create_plugin_accuracy_by_function_chart(data):
    """Create bar charts for plugin accuracy grouped by function name."""
    plugin_metrics = {}
    for row in data:
        for func in row['inputs.expected_function']:
            key = (func['function_name'], func['plugin_name'])
            plugin_metrics.setdefault(key, {'total': 0, 'correct': 0})
            plugin_metrics[key]['total'] += 1
            plugin_metrics[key]['correct'] += int(row['outputs.end_to_end_function_call.Plugin_name_accuracy'])

    plugin_data = [
        {
            'function': k[0],
            'plugin': k[1],
            'accuracy': (v['correct'] / v['total'] * 100),
            'total': v['total']
        } for k, v in plugin_metrics.items()
    ]

    charts = {}
    for fn in set(item['function'] for item in plugin_data):
        fn_data = sorted(
            [d for d in plugin_data if d['function'] == fn],
            key=lambda x: x['accuracy'],
            reverse=True
        )

        fig = go.Figure([
            go.Bar(
                x=[d['accuracy'] for d in fn_data],
                y=[d['plugin'] for d in fn_data],
                orientation='h',
                text=[f"{d['accuracy']:.0f}%<br>({d['total']} calls)" for d in fn_data],
                textposition='auto',
                marker_color='#2ecc71',
                hovertemplate="<b>%{y}</b><br>Accuracy: %{x:.1f}%<extra></extra>"
            )
        ])

        fig.update_layout(
            title=f"Plugin Accuracy for Function: {fn}",
            xaxis_title='Accuracy (%)',
            yaxis_title='Plugin Name',
            xaxis=dict(range=[0, 100]),
            showlegend=False,
            bargap=0.3
        )

        charts[fn] = fig.to_html(full_html=False)

    return charts


def generate_report(rows, metrics, template_path, output_path):
    """Generate HTML report using Jinja2 template."""
    template_dir = os.path.dirname(template_path)
    template_name = os.path.basename(template_path)

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)

    df = pd.DataFrame(rows)

    # Charts
    plugin_dist_chart = create_plugin_distribution_chart(df)
    accuracy_chart = create_accuracy_metrics_chart(metrics)
    plugin_overall_chart = create_plugin_overall_accuracy_chart(rows)

    total_queries = len(df)
    successful_queries = df['outputs.end_to_end_function_call.Overall_accuracy'].sum()
    success_rate = (successful_queries / total_queries) * 100

    html_content = template.render(
        rows=rows,
        metrics=metrics,
        agent_overall_accuracy_chart=plugin_overall_chart,
        accuracy_chart=accuracy_chart,
        function_dist_chart=plugin_dist_chart,
        total_queries=total_queries,
        successful_queries=int(successful_queries),
        success_rate=round(success_rate, 1)
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def main():
    config = load_config()
    report_config = config["report"]

    dataset_path = Path(__file__).resolve().parents[1]
    input_file = os.path.join(dataset_path, report_config["input_path"], report_config["input_file"])

    try:
        rows, metrics = load_data(input_file)

        template_path = os.path.join(
            os.path.dirname(__file__),
            report_config["template_path"],
            report_config["template_file"]
        )

        output_folder = os.path.join(dataset_path, report_config["output_path"])
        os.makedirs(output_folder, exist_ok=True)

        output_file = os.path.join(output_folder, report_config["output_file"])

        generate_report(rows, metrics, template_path, output_file)
        logger.info(f"✅ Report generated at: {output_file}")

    except FileNotFoundError as e:
        logger.error(f"❌ {e}")
    except Exception as e:
        logger.exception(f"❌ Failed to load input data.: {e}")


if __name__ == "__main__":
    main()
