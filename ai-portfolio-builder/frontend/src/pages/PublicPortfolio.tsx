import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { portfolioApi } from '../api/client';

export const PublicPortfolio = () => {
    const { slug } = useParams();
    const [data, setData] = useState<any>(null);
    const [projects, setProjects] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchPortfolio() {
            try {
                const pRes = await portfolioApi.getPublic(slug!);
                const projRes = await portfolioApi.getPublicProjects(slug!);
                setData(pRes.data);
                setProjects(projRes.data);
            } catch (e) {
                console.error("Failed to load portfolio", e);
            } finally {
                setLoading(false);
            }
        }
        fetchPortfolio();
    }, [slug]);

    if (loading) return <div className="text-center p-10">Loading Portfolio...</div>;
    if (!data) return <div className="text-center p-10">Portfolio not found or not published.</div>;

    return (
        <div className="min-h-screen bg-gray-50 text-gray-900">
            {/* Hero Section */}
            <header className="bg-white shadow-sm py-20 px-4 text-center">
                <h1 className="text-5xl font-bold mb-4">{data.title}</h1>
                <p className="text-xl text-gray-600 max-w-2xl mx-auto">{data.bio}</p>
            </header>

            {/* Projects Grid */}
            <main className="max-w-6xl mx-auto py-16 px-4">
                <h2 className="text-3xl font-bold mb-8 text-center">Featured Projects</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {projects.map((project: any) => (
                        <div key={project.id} className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow">
                            <h3 className="text-xl font-semibold mb-2">{project.name}</h3>
                            <p className="text-gray-600 mb-4">{project.description}</p>
                            <div className="flex flex-wrap gap-2 mb-4">
                                {project.tech_stack?.map((tech: string) => (
                                    <span key={tech} className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full font-medium">
                                        {tech}
                                    </span>
                                ))}
                            </div>
                            {project.link && (
                                <a href={project.link} target="_blank" className="text-blue-600 font-medium hover:underline">
                                    View Project →
                                </a>
                            )}
                        </div>
                    ))}
                </div>
            </main>
        </div>
    );
};
