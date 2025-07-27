// Fetch data from Pie chart
export async function fetchSubjectData() {
  const res = await fetch('http://localhost:9000/api/data/get_worst_subjects_data?subject=STAT');
  if (!res.ok) throw new Error("Failed to fetch subjects data");
  return await res.json();
}