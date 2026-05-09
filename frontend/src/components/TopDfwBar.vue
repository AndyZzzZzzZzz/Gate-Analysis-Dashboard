<script setup>
/* global defineProps */
import { ref, watch } from "vue";
import { fetchTopDfwCourses } from "../api";

const props = defineProps({
  subject: {
    type: String,
    default: "ALL",
  },
  levelFilter: {
    type: String,
    default: "",
  },
  facultyFilter: {
    type: String,
    default: "",
  },
  uniformColor: {
    type: Boolean,
    default: false,
  },
  minStudentsOnly: {
    type: Boolean,
    default: false,
  },
});

const loading = ref(true);
const error = ref("");
const rows = ref([]);
const selectedMetric = ref("ALL");
const metricOptions = [
  { key: "ALL", label: "All" },
  { key: "FAILURE", label: "Failure" },
  { key: "CLOWN", label: "Clown" },
];

function colorForLevel(courseCode) {
  const parts = String(courseCode || "").split(" ");
  const catalog = parts.length > 1 ? parts[1] : "";
  const firstDigit = (catalog.match(/\d/) || [null])[0];
  const palette = {
    "1": "#60a5fa",
    "2": "#34d399",
    "3": "#f59e0b",
    "4": "#f87171",
    "5": "#a78bfa",
  };
  return palette[firstDigit] || "#93c5fd";
}

function colorForSubject(courseCode) {
  const subject = String(courseCode || "").split(" ")[0];
  const fallbackPalette = ["#38bdf8", "#34d399", "#f59e0b", "#f472b6", "#a78bfa", "#fb7185", "#22c55e"];
  const hash = [...subject].reduce((acc, ch) => acc + ch.charCodeAt(0), 0);
  const subjectColors = {
    ACMA: "#38bdf8",
    CMPT: "#34d399",
    MATH: "#f59e0b",
    STAT: "#f472b6",
    BISC: "#22c55e",
    CHEM: "#eab308",
    PHYS: "#a78bfa",
    ENGL: "#60a5fa",
    BUS: "#fb7185",
  };
  return subjectColors[subject] || fallbackPalette[hash % fallbackPalette.length];
}

function resolveColor(courseCode, subject, uniformColor) {
  if (uniformColor) return "#7dd3fc";
  if (props.facultyFilter) return colorForSubject(courseCode);
  if (subject && subject !== "ALL") return colorForLevel(courseCode);
  return colorForSubject(courseCode);
}

async function loadData(subject) {
  loading.value = true;
  error.value = "";
  try {
    const selectedSubject = subject === "ALL" ? null : subject;
    const selectedFaculty = props.facultyFilter || null;
    const selectedLevel = props.levelFilter || null;
    const minStudents = props.minStudentsOnly ? 100 : null;
    const payload = await fetchTopDfwCourses(
      selectedSubject,
      selectedFaculty,
      10,
      selectedLevel,
      selectedMetric.value,
      minStudents
    );
    rows.value = (payload.courses || [])
      .map((item) => ({
      name: item.course_code,
      selectedRate: Number(((item.selected_rate || 0) * 100).toFixed(1)),
      color: resolveColor(item.course_code, subject, props.uniformColor),
      }))
      .sort((a, b) => b.selectedRate - a.selectedRate);
  } catch (err) {
    console.error(err);
    error.value = "Unable to load top DFW courses.";
    rows.value = [];
  } finally {
    loading.value = false;
  }
}

watch(
  () => [
    props.subject,
    props.facultyFilter,
    props.uniformColor,
    props.levelFilter,
    props.minStudentsOnly,
    selectedMetric.value,
  ],
  ([subject]) => {
    loadData(subject);
  },
  { immediate: true }
);

function metricLabel(metricKey) {
  const match = metricOptions.find((m) => m.key === metricKey);
  return match ? match.label : metricKey;
}

function metricDescription(metricKey) {
  if (metricKey === "FAILURE") return "D + F";
  if (metricKey === "CLOWN") return "FD + N";
  return "D + F + FD + N";
}
</script>

<template>
  <div class="chart-card">
    <div class="title-row">
      <h3>Who&apos;s Not Gonna Make It</h3>
      <div class="metric-buttons">
        <button
          v-for="metric in metricOptions"
          :key="metric.key"
          class="metric-btn"
          :class="{ active: selectedMetric === metric.key }"
          @click="selectedMetric = metric.key"
        >
          {{ metric.label }}
        </button>
      </div>
    </div>
    <p class="sub">
      Top 10 {{ metricLabel(selectedMetric) }} vibes (by course) in {{ props.subject === "ALL" ? "all subjects" : props.subject }}
      <span v-if="props.facultyFilter"> (faculty: {{ props.facultyFilter }})</span>
      <span v-if="props.levelFilter"> ({{ props.levelFilter }}-level)</span>
      <span v-if="props.minStudentsOnly"> (100+ students)</span>
      <span v-if="props.uniformColor"> (uniform color mode)</span>
      <span class="metric-details"> - {{ metricDescription(selectedMetric) }}</span>
    </p>
    <p v-if="loading" class="status">Loading...</p>
    <p v-else-if="error" class="status">{{ error }}</p>
    <p v-else-if="!rows.length" class="status">No courses found for this subject.</p>
    <div v-else class="bar-list">
      <div v-for="item in rows" :key="item.name" class="bar-row">
        <span class="label" :style="{ color: item.color }">{{ item.name }}</span>
        <div class="bar-track">
          <div :style="{ width: `${Math.max(item.selectedRate, 1)}%`, background: item.color }" class="bar-fill"></div>
        </div>
        <span class="value" :style="{ color: item.color }">{{ item.selectedRate }}%</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chart-card { width: 100%; }
h3 { margin: 0; color: #f3f4f6; }
.title-row { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.metric-buttons { display: flex; gap: 6px; flex-wrap: wrap; }
.metric-btn {
  border: 1px solid #475569;
  background: #1e293b;
  color: #cbd5e1;
  border-radius: 999px;
  font-size: 0.72rem;
  padding: 3px 8px;
  cursor: pointer;
}
.metric-btn.active {
  border-color: #38bdf8;
  color: #f0f9ff;
  background: #0f3b57;
}
.sub { margin: 4px 0 14px; color: #9ca3af; font-size: 0.9rem; }
.metric-details { color: #94a3b8; }
.status { color: #d1d5db; }
.bar-list { display: flex; flex-direction: column; gap: 10px; }
.bar-row { display: grid; grid-template-columns: 90px 1fr 56px; gap: 10px; align-items: center; }
.label, .value { color: #e5e7eb; font-size: 0.86rem; }
.bar-track { height: 12px; background: #374151; border-radius: 999px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 999px; }
</style>
