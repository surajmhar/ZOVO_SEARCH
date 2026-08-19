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

  // Initial state
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
    {
      progress: 100,
      step: 4,
      title: "Analysis complete",
      status: "Your SEO report is ready.",
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

  function showResults(url) {
    loadingSection.style.display = "none";
    resultsSection.style.display = "block";

    analyzedWebsite.textContent = `SEO analysis for ${url}`;

    analysisSteps.forEach((step) => {
      step.classList.remove("active");
      step.classList.add("complete");
    });

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

  function runDemoAnalysis(url) {
    resetProgress();
    showLoading();

    let index = 0;

    function runStage() {
      if (index >= stages.length) {
        setTimeout(() => {
          showResults(url);
        }, 700);

        return;
      }

      const stage = stages[index];

      progressBar.style.width = `${stage.progress}%`;
      percentageText.textContent = `${stage.progress}%`;

      analysisStepText.textContent = stage.title;
      analysisStatus.textContent = stage.status;

      updateAnalysisSteps(stage.step);

      index += 1;

      setTimeout(runStage, 850);
    }

    setTimeout(runStage, 500);
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const rawUrl = websiteInput.value.trim();

    if (!rawUrl) {
      websiteInput.focus();
      return;
    }

    const url = normalizeUrl(rawUrl);

    runDemoAnalysis(url);
  });

  reanalyzeButton.addEventListener("click", () => {
    loadingSection.style.display = "none";
    resultsSection.style.display = "none";

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
