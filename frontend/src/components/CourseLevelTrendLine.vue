<script setup>
import { onMounted, ref } from "vue";
import { fetchPopulationData } from "../api";

const loading = ref(true);
const error = ref("");
const points = ref([]);

const width = 560;
const height = 280;
const pad = 28;

function scale(value, min, max, outMin, outMax) {
  if (max <= min) return (outMin + outMax) / 2;
  return outMin + ((value - min) / (max - min)) * (outMax - outMin);
}

function pointsToPath(arr) {
  if (!arr.length) return "";
  return arr.map((p, idx) => `${idx === 0 ? "M" : "L"} ${p.x} ${p.y}`).join(" ");
}

async function loadData() {
  loading.value = true;
  error.value = "";
  try {
    const payload = await fetchPopulationData();
    const source = payload.course_level_difficulty || [];
    const transformed = source.map((item, idx) => ({
      label: item.course_level,
      index: idx,
      dfwRate: Number((item.withdraw_rate || 0) * 100),
      avgGpa: Number(item.avg_gpa || 0),
    }));

    const minX = 0;
    const maxX = Math.max(transformed.length - 1, 1);
    points.value = transformed.map((item) => ({
      ...item,
      x: scale(item.index, minX, maxX, pad, width - pad),
      yWithdraw: scale(item.dfwRate, 0, 40, height - pad, pad),
      yGpa: scale(item.avgGpa, 0, 4.33, height - pad, pad),
    }));
  } catch (err) {
    console.error(err);
    error.value = "Unable to load trend data.";
  } finally {
    loading.value = false;
  }
}

onMounted(loadData);
</script>

<template>
  <div class="chart-card">
    <h3>Course Level Trend</h3>
    <p class="sub">Line plot of withdrawal trend and average GPA by level</p>
    <p v-if="loading" class="status">Loading...</p>
    <p v-else-if="error" class="status">{{ error }}</p>
    <svg v-else class="plot" :viewBox="`0 0 ${width} ${height}`">
      <line :x1="pad" :y1="height - pad" :x2="width - pad" :y2="height - pad" stroke="#4b5563" />
      <line :x1="pad" :y1="pad" :x2="pad" :y2="height - pad" stroke="#4b5563" />
      <path :d="pointsToPath(points.map(p => ({ x: p.x, y: p.yWithdraw })))" stroke="#f59e0b" fill="none" stroke-width="2" />
      <path :d="pointsToPath(points.map(p => ({ x: p.x, y: p.yGpa })))" stroke="#60a5fa" fill="none" stroke-width="2" />
      <g v-for="p in points" :key="p.label">
        <circle :cx="p.x" :cy="p.yWithdraw" r="3" fill="#f59e0b" />
        <circle :cx="p.x" :cy="p.yGpa" r="3" fill="#60a5fa" />
        <text :x="p.x - 14" :y="height - 10" font-size="9" fill="#d1d5db">{{ p.label }}</text>
      </g>
    </svg>
    <div class="legend">
      <span><i class="w"></i> Withdrawal rate (%)</span>
      <span><i class="g"></i> Avg GPA</span>
    </div>
  </div>
</template>

<style scoped>
.chart-card { width: 100%; }
h3 { margin: 0; color: #f3f4f6; }
.sub { margin: 4px 0 14px; color: #9ca3af; font-size: 0.9rem; }
.status { color: #d1d5db; }
.plot { width: 100%; max-width: 560px; background: #111827; border-radius: 8px; }
.legend { margin-top: 8px; display: flex; gap: 12px; color: #d1d5db; font-size: 0.82rem; }
.legend i { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }
.legend .w { background: #f59e0b; }
.legend .g { background: #60a5fa; }
</style>
