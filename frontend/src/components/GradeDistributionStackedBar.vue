<script setup>
/* global defineProps */
import { ref, watch } from "vue";
import { fetchCourseData, fetchCourses } from "../api";

const props = defineProps({
  subject: {
    type: String,
    default: "STAT",
  },
});

const loading = ref(true);
const error = ref("");
const courses = ref([]);
const selectedCourse = ref("");
const segments = ref([]);

const gradeOrder = ["# A+", "# A", "# A-", "# B+", "# B", "# B-", "# C+", "# C", "# C-", "# D", "# F", "# W"];
const colors = {
  "# A+": "#22c55e", "# A": "#4ade80", "# A-": "#86efac",
  "# B+": "#60a5fa", "# B": "#3b82f6", "# B-": "#2563eb",
  "# C+": "#facc15", "# C": "#eab308", "# C-": "#ca8a04",
  "# D": "#f97316", "# F": "#ef4444", "# W": "#a78bfa",
};

async function loadCourses(subject) {
  const payload = await fetchCourses(subject);
  courses.value = payload.courses || [];
  selectedCourse.value = courses.value[0] || "";
}

async function loadDistribution(course) {
  if (!course) {
    segments.value = [];
    return;
  }
  const payload = await fetchCourseData(course);
  const percentages = payload.percentages || {};
  segments.value = gradeOrder
    .map((grade) => ({
      label: grade.replace("# ", ""),
      value: Number((percentages[grade] || 0) * 100),
      color: colors[grade],
    }))
    .filter((x) => x.value > 0);
}

async function refresh(subject) {
  loading.value = true;
  error.value = "";
  try {
    await loadCourses(subject);
    await loadDistribution(selectedCourse.value);
  } catch (err) {
    console.error(err);
    error.value = "Unable to load course grade distribution.";
  } finally {
    loading.value = false;
  }
}

watch(
  () => props.subject,
  (subject) => refresh(subject),
  { immediate: true }
);

watch(selectedCourse, (course) => {
  loadDistribution(course);
});
</script>

<template>
  <div class="chart-card">
    <h3>Grade Distribution</h3>
    <p class="sub">100% stacked bar for selected course</p>
    <select v-model="selectedCourse" class="select" :disabled="loading || !courses.length">
      <option v-for="course in courses" :key="course" :value="course">{{ course }}</option>
    </select>
    <p v-if="loading" class="status">Loading...</p>
    <p v-else-if="error" class="status">{{ error }}</p>
    <div v-else class="stack-wrap">
      <div class="stack-bar">
        <div
          v-for="segment in segments"
          :key="segment.label"
          class="segment"
          :style="{ width: `${segment.value}%`, background: segment.color }"
          :title="`${segment.label}: ${segment.value.toFixed(1)}%`"
        ></div>
      </div>
      <div class="legend">
        <span v-for="segment in segments" :key="segment.label" class="legend-item">
          <i :style="{ background: segment.color }"></i>{{ segment.label }} {{ segment.value.toFixed(1) }}%
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chart-card { width: 100%; }
h3 { margin: 0; color: #f3f4f6; }
.sub { margin: 4px 0 10px; color: #9ca3af; font-size: 0.9rem; }
.select { background: #111827; color: #f3f4f6; border: 1px solid #374151; border-radius: 6px; padding: 6px 8px; margin-bottom: 10px; }
.status { color: #d1d5db; }
.stack-wrap { display: flex; flex-direction: column; gap: 12px; }
.stack-bar { height: 26px; display: flex; border-radius: 8px; overflow: hidden; background: #374151; }
.segment { height: 100%; }
.legend { display: flex; flex-wrap: wrap; gap: 8px; }
.legend-item { font-size: 0.82rem; color: #e5e7eb; display: inline-flex; gap: 6px; align-items: center; }
.legend-item i { width: 10px; height: 10px; border-radius: 2px; display: inline-block; }
</style>
