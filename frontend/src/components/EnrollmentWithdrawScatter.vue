<script setup>
import { onMounted, ref } from "vue";
import { fetchPopulationData } from "../api";

const loading = ref(true);
const error = ref("");
const points = ref([]);

const width = 560;
const height = 300;
const pad = 28;

function scale(value, min, max, outMin, outMax) {
  if (max <= min) return (outMin + outMax) / 2;
  return outMin + ((value - min) / (max - min)) * (outMax - outMin);
}

async function loadData() {
  loading.value = true;
  error.value = "";
  try {
    const payload = await fetchPopulationData();
    const source = payload.top_dfw_courses || [];
    if (!source.length) {
      points.value = [];
      return;
    }

    const enrollments = source.map((x) => Number(x.total_students || 0));
    const withdrawRates = source.map((x) => Number((x.withdraw_rate || 0) * 100));
    const minEnrollment = Math.min(...enrollments);
    const maxEnrollment = Math.max(...enrollments);
    const minWithdraw = Math.min(...withdrawRates);
    const maxWithdraw = Math.max(...withdrawRates);

    points.value = source.map((item) => {
      const enroll = Number(item.total_students || 0);
      const withdraw = Number((item.withdraw_rate || 0) * 100);
      const dfw = Number((item.dfw_rate || 0) * 100);
      return {
        name: item.course_code,
        enroll,
        withdraw,
        dfw,
        x: scale(enroll, minEnrollment, maxEnrollment, pad, width - pad),
        y: scale(withdraw, minWithdraw, maxWithdraw, height - pad, pad),
        r: scale(dfw, 0, 100, 5, 14),
      };
    });
  } catch (err) {
    console.error(err);
    error.value = "Unable to load scatter data.";
  } finally {
    loading.value = false;
  }
}

onMounted(loadData);
</script>

<template>
  <div class="chart-card">
    <h3>Enrollment vs Withdraw</h3>
    <p class="sub">Bubble scatter (size = DFW rate)</p>
    <p v-if="loading" class="status">Loading...</p>
    <p v-else-if="error" class="status">{{ error }}</p>
    <svg v-else class="plot" :viewBox="`0 0 ${width} ${height}`">
      <line :x1="pad" :y1="height - pad" :x2="width - pad" :y2="height - pad" stroke="#4b5563" />
      <line :x1="pad" :y1="pad" :x2="pad" :y2="height - pad" stroke="#4b5563" />
      <g v-for="point in points" :key="point.name">
        <circle :cx="point.x" :cy="point.y" :r="point.r" fill="#60a5fa" fill-opacity="0.7" />
        <text :x="point.x + point.r + 2" :y="point.y - 2" font-size="9" fill="#e5e7eb">{{ point.name }}</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.chart-card { width: 100%; }
h3 { margin: 0; color: #f3f4f6; }
.sub { margin: 4px 0 14px; color: #9ca3af; font-size: 0.9rem; }
.status { color: #d1d5db; }
.plot { width: 100%; max-width: 560px; height: auto; background: #111827; border-radius: 8px; }
</style>
