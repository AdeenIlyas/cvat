import React, { useEffect, useState } from 'react';
import { getCore } from 'cvat-core-wrapper';
import Spin from 'antd/lib/spin';
import Card from 'antd/lib/card';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const core = getCore();

interface AnalyticsProps {
    taskId: number;
}

export default function AnalyticsComponent({ taskId }: AnalyticsProps): JSX.Element {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let mounted = true;
        setLoading(true);
        core.server.request(`/api/tasks/${taskId}/annotation_counts`, { method: 'GET' })
            .then((response: any) => {
                if (mounted) {
                    setData(response);
                    setError(null);
                    setLoading(false);
                }
            })
            .catch((err: any) => {
                if (mounted) {
                    console.error('Failed to load annotation counts', err);
                    setError('Failed to load annotation counts. You may not have permission.');
                    setLoading(false);
                }
            });
        return () => {
            mounted = false;
        };
    }, [taskId]);

    if (loading) {
        return <Spin style={{ margin: '20px auto', display: 'block' }} />;
    }

    if (error) {
        return (
            <Card title="Annotation Analytics" className="cvat-task-analytics" style={{ marginTop: 20 }}>
                <div style={{ color: 'red' }}>{error}</div>
            </Card>
        );
    }

    if (!data || Object.keys(data).length === 0) {
        return (
            <Card title="Annotation Analytics" className="cvat-task-analytics">
                <div>No annotation data available for this task.</div>
            </Card>
        );
    }

    const labels = Object.keys(data);
    
    // Find all shape types for the datasets
    const allTypes = new Set<string>();
    labels.forEach(label => {
        Object.keys(data[label].by_type).forEach(t => allTypes.add(t));
    });
    
    const colors = [
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(75, 192, 192, 0.5)',
        'rgba(153, 102, 255, 0.5)',
        'rgba(255, 159, 64, 0.5)',
    ];

    const datasets = Array.from(allTypes).map((type, index) => {
        return {
            label: type,
            data: labels.map(label => data[label].by_type[type] || 0),
            backgroundColor: colors[index % colors.length],
        };
    });

    const chartData = {
        labels,
        datasets,
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top' as const,
            },
            title: {
                display: true,
                text: 'Annotation Counts by Class and Type',
            },
        },
        scales: {
            x: {
                stacked: true,
            },
            y: {
                stacked: true,
            },
        },
    };

    return (
        <Card title="Annotation Analytics" className="cvat-task-analytics" style={{ marginTop: 20 }}>
            <Bar options={options} data={chartData} />
        </Card>
    );
}
