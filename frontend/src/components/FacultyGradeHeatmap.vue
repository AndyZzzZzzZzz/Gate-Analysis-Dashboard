<script setup>
import { computed, onMounted, ref } from "vue";
import { fetchFacultyGradeHeatmap } from "../api";

const loading = ref(true);
const error = ref("");
const faculties = ref([]);
const grades = ref([]);
const matrix = ref([]);

const minMax = computed(() => {
  const values = matrix.value.flat();
  if (!values.length) return { min: 0, max: 1 };
  return { min: Math.min(...values), max: Math.max(...values) };
});

function colorFor(value) {
  const { min, max } = minMax.value;
  const ratio = max > min ? (value - min) / (max - min) : 0;
  const alpha = 0.2 + ratio * 0.8;
  return `rgba(96, 165, 250, ${alpha})`;
}

async function loadData() {
  loading.value = true;
  error.value = "";
  try {
    const payload = await fetchFacultyGradeHeatmap();
    faculties.value = payload.faculties || [];
    grades.value = payload.grades || [];
    matrix.value = payload.matrix || [];
  } catch (err) {
    console.error(err);
    error.value = "Unable to load faculty heatmap data.";
  } finally {
    loading.value = false;
  }
}

onMounted(loadData);
</script>

<template>
  <div class="chart-card">
    <h3>Faculty Grading Profile</h3>
    <p class="sub">Heatmap of grade distribution percentages by faculty</p>
    <p v-if="loading" class="status">Loading...</p>
    <p v-else-if="error" class="status">{{ error }}</p>
    <div v-else class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Faculty</th>
            <th v-for="grade in grades" :key="grade">{{ grade.replace("# ", "") }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(faculty, rowIndex) in faculties" :key="faculty">
            <td>{{ faculty }}</td>
            <td
              v-for="(grade, colIndex) in grades"
              :key="`${faculty}-${grade}`"
              :style="{ backgroundColor: colorFor(matrix[rowIndex][colIndex]) }"
            >
              {{ (matrix[rowIndex][colIndex] * 100).toFixed(1) }}%
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.chart-card { width: 100%; }
h3 { margin: 0; color: #f3f4f6; }
.sub { margin: 4px 0 14px; color: #9ca3af; font-size: 0.9rem; }
.status { color: #d1d5db; }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 0.8rem; color: #e5e7eb; }
th, td { border: 1px solid #374151; padding: 6px 8px; text-align: center; white-space: nowrap; }
th:first-child, td:first-child { text-align: left; background: #111827; position: sticky; left: 0; }
thead th { background: #1f2937; }
</style>
