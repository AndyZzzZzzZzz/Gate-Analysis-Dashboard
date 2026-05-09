<template>
  <div id="app" class="dashboard-shell">
    <HeaderSection />
    <main class="main-content">
      <section class="dashboard-rows">
        <article class="dashboard-row">
          <div class="panel panel-info">
            <h3>NGMI Ranking</h3>
            <p>
              Feel free to explore what percentage of students—across faculties, subjects, and whole
              classes—were clearly not born for university and, if we&apos;re honest, are not gonna
              make it in the end. Tweak the filters; the bars don&apos;t judge (we do, a little).
            </p>
            <div class="filter-stack">
              <div class="toggle-group">
                <select v-model="topDfwSubjectSelect" class="select" @change="applyTopDfwSubjectSelection">
                  <option value="">Select subject...</option>
                  <option v-for="subject in subjectOptions" :key="subject" :value="subject">
                    {{ subject }}
                  </option>
                </select>
                <button
                  class="toggle-btn"
                  :class="{ active: topDfwSubject === 'ALL' }"
                  @click="setTopDfwAllSubjects"
                >
                  All Subjects
                </button>
                <button
                  class="toggle-btn"
                  :class="{ active: topDfwUniformColor }"
                  @click="topDfwUniformColor = !topDfwUniformColor"
                >
                  Uniform Color
                </button>
                <button
                  class="toggle-btn"
                  :class="{ active: topDfwMin100 }"
                  @click="topDfwMin100 = !topDfwMin100"
                >
                  100+
                </button>
                <select v-model="topDfwLevelFilter" class="select level-select">
                  <option value="">All levels</option>
                  <option value="100">100-level</option>
                  <option value="200">200-level</option>
                  <option value="300">300-level</option>
                  <option value="400">400-level</option>
                </select>
              </div>
              <div class="toggle-group">
                <select v-model="topDfwFacultyFilter" class="select">
                  <option value="">All faculties</option>
                  <option v-for="faculty in facultyOptions" :key="faculty" :value="faculty">
                    {{ faculty }}
                  </option>
                </select>
              </div>
            </div>
          </div>
          <div class="panel panel-graph">
            <TopDfwBar
              :subject="topDfwSubject"
              :faculty-filter="topDfwFacultyFilter"
              :uniform-color="topDfwUniformColor"
              :level-filter="topDfwLevelFilter"
              :min-students-only="topDfwMin100"
            />
          </div>
        </article>

        <article class="dashboard-row row-reverse">
          <div class="panel panel-graph">
            <EnrollmentWithdrawScatter />
          </div>
          <div class="panel panel-info">
            <h3>Enrollment vs Withdraw</h3>
            <p>
              Bubble size represents DFW pressure. This highlights large classes with high dropout risk.
            </p>
          </div>
        </article>

        <article class="dashboard-row">
          <div class="panel panel-info">
            <h3>Grade Distribution</h3>
            <p>
              100% stacked bar shows grade composition for a selected course under this subject.
            </p>
          </div>
          <div class="panel panel-graph">
            <GradeDistributionStackedBar :subject="selectedSubject" />
          </div>
        </article>

        <article class="dashboard-row row-reverse">
          <div class="panel panel-graph">
            <CourseLevelTrendLine />
          </div>
          <div class="panel panel-info">
            <h3>Course Level Trend</h3>
            <p>
              Compares GPA and withdrawal behavior from 100-level to 400-level classes.
            </p>
          </div>
        </article>

        <article class="dashboard-row">
          <div class="panel panel-info">
            <h3>Faculty Grading Profile</h3>
            <p>
              Heatmap compares faculty-level grade distributions to reveal grading patterns at a glance.
            </p>
          </div>
          <div class="panel panel-graph">
            <FacultyGradeHeatmap />
          </div>
        </article>

        <article class="dashboard-row row-reverse">
          <div class="panel panel-graph">
            <CourseComparisonRadar :subject="selectedSubject" />
          </div>
          <div class="panel panel-info">
            <h3>Course Comparison Radar</h3>
            <p>
              A fun quick-compare widget for two courses using DFW, withdrawals, failure share, A-range, and GPA.
            </p>
          </div>
        </article>
      </section>
    </main>
    <FooterSection />
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import HeaderSection from "./components/HeaderSection.vue";
import FooterSection from "./components/FooterSection.vue";
import TopDfwBar from "./components/TopDfwBar.vue";
import EnrollmentWithdrawScatter from "./components/EnrollmentWithdrawScatter.vue";
import GradeDistributionStackedBar from "./components/GradeDistributionStackedBar.vue";
import CourseLevelTrendLine from "./components/CourseLevelTrendLine.vue";
import FacultyGradeHeatmap from "./components/FacultyGradeHeatmap.vue";
import CourseComparisonRadar from "./components/CourseComparisonRadar.vue";
import { fetchFaculties, fetchSubjects } from "./api";

const subjectOptions = ref(["STAT", "ACMA", "MATH", "CMPT"]);
const facultyOptions = ref([]);
const selectedSubject = ref("STAT");
const topDfwSubjectSelect = ref("");
const topDfwSubject = ref("ALL");
const topDfwFacultyFilter = ref("");
const topDfwUniformColor = ref(false);
const topDfwLevelFilter = ref("");
const topDfwMin100 = ref(true);

function applyTopDfwSubjectSelection() {
  if (!topDfwSubjectSelect.value) {
    topDfwSubject.value = "ALL";
    return;
  }
  topDfwSubject.value = topDfwSubjectSelect.value;
  selectedSubject.value = topDfwSubjectSelect.value;
}

function setTopDfwAllSubjects() {
  topDfwSubject.value = "ALL";
  topDfwSubjectSelect.value = "";
}

onMounted(async () => {
  try {
    const [subjectPayload, facultyPayload] = await Promise.all([fetchSubjects(), fetchFaculties()]);

    if (Array.isArray(subjectPayload.subjects) && subjectPayload.subjects.length > 0) {
      subjectOptions.value = subjectPayload.subjects;
      if (!subjectPayload.subjects.includes(selectedSubject.value)) {
        selectedSubject.value = subjectPayload.subjects[0];
      }
    }

    if (Array.isArray(facultyPayload.faculties) && facultyPayload.faculties.length > 0) {
      facultyOptions.value = facultyPayload.faculties;
    }
  } catch (error) {
    console.error("Failed to load subjects:", error);
  }
});
</script>

<style>
html,
body,
#app {
  margin: 0;
  padding: 0;
  min-height: 100%;
  background: #121212;
}

.dashboard-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #121212;
  color: #f5f5f5;
}

.main-content {
  flex: 1;
  display: flex;
  justify-content: center;
  padding: 20px;
}

.dashboard-rows {
  width: min(1400px, 100%);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.dashboard-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  min-height: 360px;
}

.panel {
  background: #1a1a1a;
  border: 1px solid #2d2d2d;
  border-radius: 14px;
  padding: 20px;
}

.panel-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 12px;
}

.panel-info h3 {
  margin: 0;
  font-size: 1.4rem;
}

.panel-info p {
  margin: 0;
  color: #d2d2d2;
  line-height: 1.5;
}

.toggle-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-stack {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.select {
  width: 180px;
  border: 1px solid #4a4a4a;
  background: #252525;
  color: #f2f2f2;
  border-radius: 8px;
  padding: 8px 10px;
}

.toggle-btn {
  border: 1px solid #4a4a4a;
  background: #252525;
  color: #f2f2f2;
  border-radius: 999px;
  padding: 8px 14px;
  cursor: pointer;
}

.toggle-btn.active {
  border-color: #5d9dff;
  background: #1f3f6d;
}

.panel-graph {
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.row-reverse .panel-info {
  order: 2;
}

.row-reverse .panel-graph {
  order: 1;
}

@media (max-width: 1000px) {
  .dashboard-row {
    grid-template-columns: 1fr;
  }

  .row-reverse .panel-info,
  .row-reverse .panel-graph {
    order: unset;
  }
}
</style>