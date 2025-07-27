// Fetch data from Pie chartw
export async function fetchChartData() {
  const res = await fetch('http://localhost:8000/api/data');
  if (!res.ok) throw new Error("Failed to fetch chart data");
  return await res.json();
}