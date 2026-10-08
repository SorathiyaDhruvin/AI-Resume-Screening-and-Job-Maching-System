import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiClient } from '../../api/apiClient';
import { Check, X, ArrowLeft, Download, Award, ChevronDown, ChevronUp } from 'lucide-react';

export default function JobScreening() {
  const { jobId } = useParams<{ jobId: string }>();
  const [job, setJob] = useState<any>(null);
  const [matches, setMatches] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedRow, setExpandedRow] = useState<number | null>(null);

  useEffect(() => {
    fetchData();
  }, [jobId]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [jobRes, matchesRes] = await Promise.all([
        apiClient.get(`/jobs/${jobId}`),
        apiClient.get(`/matching/job/${jobId}`)
      ]);
      setJob(jobRes.data);
      setMatches(matchesRes.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-center">Loading AI Matches...</div>;

  return (
    <div className="space-y-6">
      <Link to="/recruiter/dashboard" className="text-gray-500 hover:text-gray-900 inline-flex items-center text-sm font-medium transition-colors">
        <ArrowLeft className="h-4 w-4 mr-1" /> Back to Dashboard
      </Link>
      
      {job && (
        <header className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{job.title}</h1>
              <p className="text-gray-500 mt-1">{job.company} • {job.location}</p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500 font-medium">Total Candidates</div>
              <div className="text-2xl font-bold text-gray-900">{matches.length}</div>
            </div>
          </div>
        </header>
      )}

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 bg-gray-50/50 flex justify-between items-center">
          <h2 className="text-lg font-bold text-gray-800">AI Ranked Candidates</h2>
          <div className="flex gap-2">
            <span className="text-xs bg-gray-100 text-gray-600 px-3 py-1.5 rounded-md font-medium">Sorted by Match Score</span>
          </div>
        </div>

        <div className="divide-y divide-gray-100">
          {matches.length === 0 ? (
            <div className="p-12 text-center text-gray-500">
              <Award className="h-12 w-12 mx-auto text-gray-300 mb-4" />
              <p>No matches generated yet.</p>
              <p className="text-sm mt-1">Wait for candidates to apply or run manual screening.</p>
            </div>
          ) : (
            matches.map((match, index) => (
              <div key={match.id} className="transition-colors hover:bg-gray-50">
                <div 
                  className="p-6 flex items-center gap-6 cursor-pointer"
                  onClick={() => setExpandedRow(expandedRow === match.id ? null : match.id)}
                >
                  <div className="shrink-0 w-12 text-center">
                    <span className="text-xl font-black text-gray-300">#{index + 1}</span>
                  </div>
                  
                  <div className="flex-1">
                    <h3 className="font-bold text-lg text-gray-900">{match.candidate?.name || 'Unknown Candidate'}</h3>
                    <div className="text-sm text-gray-500 mt-1 flex gap-3">
                      <span>{match.candidate?.email}</span>
                    </div>
                  </div>

                  <div className="shrink-0 text-center px-6">
                    <div className="text-xs text-gray-500 font-medium uppercase tracking-wider mb-1">Match</div>
                    <div className={`text-2xl font-black ${
                      match.final_score > 0.8 ? 'text-green-600' : 
                      match.final_score > 0.6 ? 'text-yellow-600' : 'text-red-600'
                    }`}>
                      {Math.round(match.final_score * 100)}%
                    </div>
                  </div>

                  <div className="shrink-0 flex gap-2">
                    <button className="p-2 text-gray-400 hover:text-green-600 bg-white hover:bg-green-50 rounded-lg border border-gray-200 transition-colors tooltip" title="Shortlist">
                      <Check className="h-5 w-5" />
                    </button>
                    <button className="p-2 text-gray-400 hover:text-red-600 bg-white hover:bg-red-50 rounded-lg border border-gray-200 transition-colors tooltip" title="Reject">
                      <X className="h-5 w-5" />
                    </button>
                    <button className="p-2 text-gray-400 hover:text-gray-900 bg-white hover:bg-gray-100 rounded-lg border border-gray-200 transition-colors">
                      {expandedRow === match.id ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
                    </button>
                  </div>
                </div>

                {/* Expanded Details */}
                {expandedRow === match.id && (
                  <div className="px-6 pb-6 pt-0 ml-16 border-t border-gray-100 mt-2">
                    <div className="pt-4 grid grid-cols-1 md:grid-cols-2 gap-8">
                      <div>
                        <h4 className="text-sm font-bold text-gray-900 mb-3 uppercase tracking-wider">Score Breakdown</h4>
                        <div className="space-y-3">
                          <div>
                            <div className="flex justify-between text-sm mb-1">
                              <span className="text-gray-600">Semantic AI Match</span>
                              <span className="font-bold text-gray-900">{Math.round(match.semantic_score * 100)}%</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div className="bg-primary-500 h-2 rounded-full" style={{ width: `${Math.round(match.semantic_score * 100)}%` }}></div>
                            </div>
                          </div>
                          <div>
                            <div className="flex justify-between text-sm mb-1">
                              <span className="text-gray-600">Required Skills</span>
                              <span className="font-bold text-gray-900">{Math.round(match.skill_score * 100)}%</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div className="bg-primary-500 h-2 rounded-full" style={{ width: `${Math.round(match.skill_score * 100)}%` }}></div>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div>
                        <h4 className="text-sm font-bold text-gray-900 mb-3 uppercase tracking-wider">Skill Analysis</h4>
                        <div className="mb-4">
                          <span className="text-xs text-green-600 font-bold mb-2 block">✓ MATCHED SKILLS</span>
                          <div className="flex flex-wrap gap-2">
                            {match.matched_skills?.map((skill: string, i: number) => (
                              <span key={i} className="bg-green-50 text-green-700 text-xs px-2 py-1 rounded border border-green-200">{skill}</span>
                            ))}
                            {(!match.matched_skills || match.matched_skills.length === 0) && (
                              <span className="text-xs text-gray-500">None</span>
                            )}
                          </div>
                        </div>
                        <div>
                          <span className="text-xs text-red-600 font-bold mb-2 block">✕ MISSING SKILLS</span>
                          <div className="flex flex-wrap gap-2">
                            {match.missing_skills?.map((skill: string, i: number) => (
                              <span key={i} className="bg-red-50 text-red-700 text-xs px-2 py-1 rounded border border-red-200">{skill}</span>
                            ))}
                            {(!match.missing_skills || match.missing_skills.length === 0) && (
                              <span className="text-xs text-gray-500">None</span>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="mt-6 pt-4 border-t border-gray-100 flex justify-end">
                      <button className="text-sm font-medium text-primary-600 hover:text-primary-800 flex items-center">
                        <Download className="h-4 w-4 mr-2" /> Download Original Resume
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
