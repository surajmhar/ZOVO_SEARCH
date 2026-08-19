document.addEventListener("DOMContentLoaded", () => {
  console.log("Analyzer JS loaded");

  const form = document.getElementById("seoAnalyzerForm");
  const websiteInput = document.getElementById("websiteUrl");

  const heroSection = document.getElementById("seo-analyzer");
  const loadingSection = document.getElementById("analysisLoading");
  const resultsSection = document.getElementById("analyzerResults");

  const progressBar = document.getElementById("analysisProgress");
  const percentageText = document.getElementById("analysisPercentage");
  const analysisStepText = document.getElementById("analysisStep");
  const analysisStatus = document.getElementById("analysisStatus");

  const analyzedWebsite = document.getElementById("analyzedWebsite");
  const reanalyzeButton = document.getElementById("reanalyzeButton");

  const analysisSteps = document.querySelectorAll(".analysis-step");

  const overallScore = document.getElementById("overallScore");
  const scoreStatus = document.getElementById("scoreStatus");

  const performanceScore = document.getElementById("performanceScore");
  const onPageScore = document.getElementById("onPageScore");
  const technicalScore = document.getElementById("technicalScore");
  const mobileScore = document.getElementById("mobileScore");

  const performanceProgress = document.getElementById("performanceProgress");
  const onPageProgress = document.getElementById("onPageProgress");
  const technicalProgress = document.getElementById("technicalProgress");
  const mobileProgress = document.getElementById("mobileProgress");

  const passedCount = document.getElementById("passedCount");
  const warningCount = document.getElementById("warningCount");
  const criticalCount = document.getElementById("criticalCount");

  const issueList = document.querySelector(".seo-issue-list");
  const recommendationGrid = document.querySelector(".recommendation-grid");

  let currentAnalysisData = null;
  let progressTimer = null;

  loadingSection.style.display = "none";
  resultsSection.style.display = "none";

  const stages = [
    {
      progress: 12,
      step: 1,
      title: "Connecting to website...",
      status: "Checking whether the website is accessible.",
    },
    {
      progress: 28,
      step: 1,
      title: "Website connected",
      status: "Preparing the website for SEO analysis.",
    },
    {
      progress: 46,
      step: 2,
      title: "Analyzing on-page SEO...",
      status: "Checking metadata, headings and page structure.",
    },
    {
      progress: 64,
      step: 3,
      title: "Checking technical SEO...",
      status: "Reviewing technical signals and website health.",
    },
    {
      progress: 82,
      step: 4,
      title: "Generating SEO insights...",
      status: "Preparing recommendations and optimization opportunities.",
    },
  ];

  function normalizeUrl(url) {
    let value = url.trim();

    if (!/^https?:\/\//i.test(value)) {
      value = `https://${value}`;
    }

    return value;
  }

  function resetAnalysisSteps() {
    analysisSteps.forEach((step) => {
      step.classList.remove("active", "complete");
    });
  }

  function updateAnalysisSteps(currentStep) {
    analysisSteps.forEach((step) => {
      const stepNumber = Number(step.dataset.step);

      if (stepNumber < currentStep) {
        step.classList.remove("active");
        step.classList.add("complete");
      } else if (stepNumber === currentStep) {
        step.classList.remove("complete");
        step.classList.add("active");
      } else {
        step.classList.remove("active", "complete");
      }
    });
  }

  function resetProgress() {
    if (progressTimer) {
      clearTimeout(progressTimer);
      progressTimer = null;
    }

    progressBar.style.width = "0%";
    percentageText.textContent = "0%";

    analysisStepText.textContent = "Initializing analysis...";
    analysisStatus.textContent =
      "Connecting to your website and preparing SEO analysis.";

    resetAnalysisSteps();
  }

  function showLoading() {
    resultsSection.style.display = "none";
    loadingSection.style.display = "block";

    setTimeout(() => {
      loadingSection.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }, 100);
  }

  function completeProgress() {
    progressBar.style.width = "100%";
    percentageText.textContent = "100%";

    analysisStepText.textContent = "Analysis complete";
    analysisStatus.textContent = "Your SEO report is ready.";

    analysisSteps.forEach((step) => {
      step.classList.remove("active");
      step.classList.add("complete");
    });
  }

  function showResults(url) {
    loadingSection.style.display = "none";
    resultsSection.style.display = "block";

    analyzedWebsite.textContent = `SEO analysis for ${url}`;

    if (typeof lucide !== "undefined") {
      lucide.createIcons();
    }

    setTimeout(() => {
      resultsSection.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }, 150);
  }

  function runLoadingAnimation() {
    let index = 0;

    function runStage() {
      if (index >= stages.length) {
        return;
      }

      const stage = stages[index];

      progressBar.style.width = `${stage.progress}%`;
      percentageText.textContent = `${stage.progress}%`;

      analysisStepText.textContent = stage.title;
      analysisStatus.textContent = stage.status;

      updateAnalysisSteps(stage.step);

      index += 1;

      progressTimer = setTimeout(runStage, 700);
    }

    progressTimer = setTimeout(runStage, 300);
  }

  function getScoreStatus(score) {
    if (score >= 90) return "Excellent";
    if (score >= 75) return "Good";
    if (score >= 60) return "Needs Improvement";
    return "Poor";
  }

  function getIssueCounts(recommendations) {
    let warnings = 0;
    let critical = 0;

    recommendations.forEach((item) => {
      if (item.type === "error") {
        critical += 1;
      }

      if (item.type === "warning") {
        warnings += 1;
      }
    });

    const totalChecks = 10;
    const failedChecks = warnings + critical;

    return {
      passed: Math.max(totalChecks - failedChecks, 0),
      warnings,
      critical,
    };
  }

  function renderIssues(recommendations) {
    issueList.innerHTML = "";

    if (!recommendations || recommendations.length === 0) {
      issueList.innerHTML = `
        <div class="seo-issue passed">
          <div class="issue-status">
            <i data-lucide="check-circle-2"></i>
          </div>

          <div class="issue-content">
            <div class="issue-heading">
              <h4>No Major SEO Issues Found</h4>
              <span>Passed</span>
            </div>

            <p>
              The analyzed page passed the current SEO checks.
            </p>
          </div>
        </div>
      `;

      return;
    }

    recommendations.forEach((item) => {
      let cssClass = "warning";
      let icon = "triangle-alert";
      let label = "Warning";

      if (item.type === "error") {
        cssClass = "critical";
        icon = "circle-alert";
        label = "Critical";
      }

      if (item.type === "success") {
        cssClass = "passed";
        icon = "check-circle-2";
        label = "Passed";
      }

      const issue = document.createElement("div");
      issue.className = `seo-issue ${cssClass}`;

      issue.innerHTML = `
        <div class="issue-status">
          <i data-lucide="${icon}"></i>
        </div>

        <div class="issue-content">
          <div class="issue-heading">
            <h4>${item.title}</h4>
            <span>${label}</span>
          </div>

          <p>${item.message}</p>
        </div>
      `;

      issueList.appendChild(issue);
    });
  }

  function renderRecommendations(recommendations) {
    recommendationGrid.innerHTML = "";

    const actionableItems = recommendations
      .filter((item) => item.type !== "success")
      .slice(0, 3);

    if (actionableItems.length === 0) {
      actionableItems.push({
        title: "Maintain Your SEO Health",
        message:
          "Continue monitoring metadata, content structure, technical SEO and search performance.",
      });
    }

    actionableItems.forEach((item, index) => {
      const card = document.createElement("div");
      card.className = "recommendation-card";

      card.innerHTML = `
        <span class="recommendation-number">
          ${String(index + 1).padStart(2, "0")}
        </span>

        <h4>${item.title}</h4>

        <p>${item.message}</p>
      `;

      recommendationGrid.appendChild(card);
    });
  }

  function populateResults(data) {
    const categoryScores = data.category_scores;
    const counts = getIssueCounts(data.recommendations);

    overallScore.textContent = data.score;
    scoreStatus.textContent = getScoreStatus(data.score);

    performanceScore.textContent = categoryScores.performance;

    onPageScore.textContent = categoryScores.on_page;

    technicalScore.textContent = categoryScores.technical;

    mobileScore.textContent = categoryScores.mobile;

    performanceProgress.style.width = `${categoryScores.performance}%`;

    onPageProgress.style.width = `${categoryScores.on_page}%`;

    technicalProgress.style.width = `${categoryScores.technical}%`;

    mobileProgress.style.width = `${categoryScores.mobile}%`;

    passedCount.textContent = counts.passed;
    warningCount.textContent = counts.warnings;
    criticalCount.textContent = counts.critical;

    renderIssues(data.recommendations);
    renderRecommendations(data.recommendations);

    if (typeof lucide !== "undefined") {
      lucide.createIcons();
    }
  }

  async function analyzeWebsite(url) {
    resetProgress();
    showLoading();
    runLoadingAnimation();

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: url,
        }),
      });

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(result.error || "Unable to analyze this website.");
      }

      currentAnalysisData = result.data;

      console.log("Real SEO analysis:", currentAnalysisData);

      populateResults(currentAnalysisData);

      if (progressTimer) {
        clearTimeout(progressTimer);
        progressTimer = null;
      }

      completeProgress();

      setTimeout(() => {
        showResults(currentAnalysisData.final_url || url);
      }, 700);
    } catch (error) {
      console.error("Analyzer error:", error);

      if (progressTimer) {
        clearTimeout(progressTimer);
        progressTimer = null;
      }

      loadingSection.style.display = "none";

      alert(
        error.message || "Something went wrong while analyzing the website.",
      );

      heroSection.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const rawUrl = websiteInput.value.trim();

    if (!rawUrl) {
      websiteInput.focus();
      return;
    }

    const url = normalizeUrl(rawUrl);

    analyzeWebsite(url);
  });

  reanalyzeButton.addEventListener("click", () => {
    if (progressTimer) {
      clearTimeout(progressTimer);
      progressTimer = null;
    }

    loadingSection.style.display = "none";
    resultsSection.style.display = "none";

    currentAnalysisData = null;

    resetProgress();

    websiteInput.value = "";

    heroSection.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });

    setTimeout(() => {
      websiteInput.focus();
    }, 700);
  });
});
