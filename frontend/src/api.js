const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || "http://localhost:9000";

async function getJson(path) {
  const res = await fetch(`${API_BASE_URL}${path}`);
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }
  return await res.json();
}

export async function fetchSubjectData(subject = "STAT") {
  const query = encodeURIComponent(subject);
  return getJson(`/api/data/get_worst_subjects_data?subject=${query}`);
}

export async function fetchSubjects(faculty = null) {
  const suffix = faculty ? `?faculty=${encodeURIComponent(faculty)}` : "";
  return getJson(`/api/data/get_subjects${suffix}`);
}

export async function fetchFaculties() {
  return getJson("/api/data/get_faculties");
}

export async function fetchPopulationData() {
  return getJson("/api/data/get_population_data");
}

export async function fetchCourses(subject = null) {
  const suffix = subject ? `?subject=${encodeURIComponent(subject)}` : "";
  return getJson(`/api/data/get_courses${suffix}`);
}

export async function fetchCourseData(course) {
  const query = encodeURIComponent(course);
  return getJson(`/api/data/get_course_data?course=${query}`);
}

export async function fetchFacultyGradeHeatmap() {
  return getJson("/api/data/get_faculty_grade_heatmap");
}

export async function fetchTopDfwCourses(
  subject = null,
  faculty = null,
  limit = 10,
  level = null,
  metric = "ALL",
  minStudents = null
) {
  const params = new URLSearchParams();
  if (subject) params.set("subject", subject);
  if (faculty) params.set("faculty", faculty);
  if (level) params.set("level", level);
  if (metric) params.set("metric", metric);
  if (minStudents !== null && minStudents !== undefined) params.set("min_students", String(minStudents));
  params.set("limit", String(limit));
  return getJson(`/api/data/get_top_dfw_courses?${params.toString()}`);
}