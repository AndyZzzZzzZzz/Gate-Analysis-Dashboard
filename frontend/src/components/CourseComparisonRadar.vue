<script setup>
/* global defineProps */
import { computed, ref, watch } from "vue";
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
const courseA = ref("");
const courseB = ref("");
const metricsA = ref([]);
const metricsB = ref([]);

const labels = ["DFW%", "Withdraw%", "Fail%", "A-range%", "GPA"];

const pathA = computed(() => toPath(metricsA.value));
const pathB = computed(() => toPath(metricsB.value));

function toPath(values) {
  if (!values.length) return "";
  const cx = 160;
  const cy = 160;
  const r = 110;
  const points = values.map((value, idx) => {
    const angle = (-Math.PI / 2) + (idx * 2 * Math.PI) / values.length;
    const rr = (value / 100) * r;
    return [cx + rr * Math.cos(angle), cy + rr * Math.sin(angle)];
  });
  return `${points.map((p, i) => `${i === 0 ? "M" : "L"} ${p[0]} ${p[1]}`).join(" ")} Z`;
}

function toRadarMetrics(data) {
  const percentages = data.percentages || {};
  const gpaScaled = ((data.avg_gpa || 0) / 4.33) * 100;
  const failPct = ((percentages["# D"] || 0) + (percentages["# F"] || 0)) * 100;
  const aRangePct = ((percentages["# A+"] || 0) + (percentages["# A"] || 0) + (percentages["# A-"] || 0)) * 100;
  return [
    Number(((data.dfw_rate || 0) * 100).toFixed(1)),
    Number(((data.withdraw_rate || 0) * 100).toFixed(1)),
    Number(failPct.toFixed(1)),
    Number(aRangePct.toFixed(1)),
    Number(gpaScaled.toFixed(1)),
  ];
}

async function loadCourseList(subject) {
  const payload = await fetchCourses(subject);
  courses.value = payload.courses || [];
  courseA.value = courses.value[0] || "";
  courseB.value = courses.value[1] || courses.value[0] || "";
}

async function loadComparison() {
  if (!courseA.value || !courseB.value) return;
  const [a, b] = await Promise.all([fetchCourseData(courseA.value), fetchCourseData(courseB.value)]);
  metricsA.value = toRadarMetrics(a);
  metricsB.value = toRadarMetrics(b);
}

async function refresh(subject) {
  loading.value = true;
  error.value = "";
  try {
    await loadCourseList(subject);
    await loadComparison();
  } catch (err) {
    console.error(err);
    error.value = "Unable to load radar comparison.";
  } finally {
    loading.value = false;
  }
}

watch(
  () => props.subject,
  (subject) => refresh(subject),
  { immediate: true }
);

watch([courseA, courseB], () => {
  loadComparison();
});
</script>

<template>
  <div class="chart-card">
    <h3>Course Comparison Radar</h3>
    <p class="sub">Fun side-by-side profile for two courses</p>
    <div class="controls">
      <select v-model="courseA" class="select" :disabled="loading || !courses.length">
        <option v-for="course in courses" :key="`a-${course}`" :value="course">{{ course }}</option>
      </select>
      <select v-model="courseB" class="select" :disabled="loading || !courses.length">
        <option v-for="course in courses" :key="`b-${course}`" :value="course">{{ course }}</option>
      </select>
    </div>
    <p v-if="loading" class="status">Loading...</p>
    <p v-else-if="error" class="status">{{ error }}</p>
    <svg v-else class="radar" viewBox="0 0 320 320">
      <polygon points="160,50 264,106 264,214 160,270 56,214 56,106" fill="none" stroke="#374151" />
      <polygon points="160,80 236,120 236,200 160,240 84,200 84,120" fill="none" stroke="#374151" />
      <polygon points="160,110 208,134 208,186 160,210 112,186 112,134" fill="none" stroke="#374151" />
      <path :d="pathA" fill="#60a5fa66" stroke="#60a5fa" stroke-width="2" />
      <path :d="pathB" fill="#f59e0b55" stroke="#f59e0b" stroke-width="2" />
      <text x="147" y="18" fill="#d1d5db" font-size="10">{{ labels[0] }}</text>
      <text x="286" y="104" fill="#d1d5db" font-size="10">{{ labels[1] }}</text>
      <text x="286" y="220" fill="#d1d5db" font-size="10">{{ labels[2] }}</text>
      <text x="146" y="312" fill="#d1d5db" font-size="10">{{ labels[3] }}</text>
      <text x="14" y="220" fill="#d1d5db" font-size="10">{{ labels[4] }}</text>
    </svg>
    <div class="legend">
      <span><i class="a"></i>{{ courseA }}</span>
      <span><i class="b"></i>{{ courseB }}</span>
    </div>
  </div>
</template>

<style scoped>
.chart-card { width: 100%; }
h3 { margin: 0; color: #f3f4f6; }
.sub { margin: 4px 0 10px; color: #9ca3af; font-size: 0.9rem; }
.controls { display: flex; gap: 8px; margin-bottom: 10px; }
.select { background: #111827; color: #f3f4f6; border: 1px solid #374151; border-radius: 6px; padding: 6px 8px; }
.status { color: #d1d5db; }
.radar { width: 100%; max-width: 360px; background: #111827; border-radius: 8px; }
.legend { margin-top: 8px; display: flex; gap: 12px; font-size: 0.82rem; color: #d1d5db; }
.legend i { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }
.legend .a { background: #60a5fa; }
.legend .b { background: #f59e0b; }
</style>
