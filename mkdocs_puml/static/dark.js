/**
 * mkdocs-puml plugin - Auto Dark Mode Script
 * ==========================================
 *
 * This script is designed to work with the mkdocs-puml plugin and the
 * mkdocs-material theme to automatically switch between light and dark themes.
 *
 * Dependencies:
 * -------------
 * - The script requires the mkdocs-puml plugin to be installed and configured
 *   in the MkDocs project.
 * - The script is intended to be used with the mkdocs-material theme.
 *
 * Description:
 * ------------
 * The script listens for changes in the system preference for dark mode and
 * updates the theme accordingly. It also listens for changes in the MkDocs
 * theme preference and updates the theme based on the user's selection.
 * The script toggles the visibility of PlantUML divs based on the theme to ensure
 * that the correct image is displayed.
 *
 */

// Set this flag to true for debugging output, false to suppress logs
const DEBUG = true;

/**
 * Helper function for controlled logging.
 * @param {string} message - The message to log.
 */
function log(message) {
  if (DEBUG) {
    console.log(message);
  }
}

/**
 * Retrieves the current theme state based on system preferences.
 * @returns {string} - The current theme state ('dark' or 'light').
 */
function getThemeState() {
  const systemPreference = window.matchMedia("(prefers-color-scheme: dark)")
    .matches
    ? "dark"
    : "light";
  log(`🌐 System Preference: ${systemPreference}`);
  return systemPreference;
}

/**
 * Retrieves the current theme state based on the data attribute on the body.
 * @returns {string} - The current theme state ('dark', 'light', or 'auto').
 */
function getMkdocsThemeState() {
  const colorScheme = document.body.getAttribute("data-md-color-media");

  let themeState;
  switch (colorScheme) {
    case "(prefers-color-scheme: dark)":
      themeState = "dark";
      break;
    case "(prefers-color-scheme: light)":
      themeState = "light";
      break;
    case "(prefers-color-scheme)":
      themeState = "auto";
      break;
    default:
      themeState = getThemeState();
      break;
  }

  log(`📋 Mkdocs Preference: ${themeState}`);
  return themeState;
}

/**
 * Updates the theme based on the provided mode.
 * @param {string} mode - The theme mode ('dark' or 'light').
 */
function updateTheme(mode) {
  log(`🔄 Updating theme`);
  togglePumlVisibility(mode);
}

/**
 * Toggles the visibility of PUML divs based on the theme.
 * @param {string} mode - The theme mode ('dark' or 'light').
 */
function togglePumlVisibility(mode) {
  const lightDivs = document.querySelectorAll(`[data-puml-theme="light"]`);
  const darkDivs = document.querySelectorAll(`[data-puml-theme="dark"]`);

  lightDivs.forEach((div) => {
    div.style.display = mode === "light" ? "block" : "none";
  });

  darkDivs.forEach((div) => {
    div.style.display = mode === "dark" ? "block" : "none";
  });

  log(`🌓 PUML visibility toggled to ${mode} mode.`);
}

// Main script logic
document.addEventListener("DOMContentLoaded", () => {
  // Handle initial theme setup
  const mkdocsTheme = getMkdocsThemeState();
  const systemTheme = getThemeState();
  let currentTheme;

  if (mkdocsTheme === "auto") {
    currentTheme = systemTheme;
  } else {
    currentTheme = mkdocsTheme;
  }

  updateTheme(currentTheme);

  // Listen for system preference changes if the theme is set to 'auto'
  const darkModeMediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
  darkModeMediaQuery.addEventListener("change", (e) => {
    const newTheme = e.matches ? "dark" : "light";
    log(`⚡ System preference changed to: ${newTheme} mode`);
    // if not in auto mode, do nothing
    if (getMkdocsThemeState() === "auto") {
      updateTheme(newTheme);
    }
  });

  // Set up event listeners for the theme toggle inputs
  document.querySelectorAll('input[name="__palette"]').forEach((input) => {
    input.addEventListener("change", () => {
      log(`⚡ Mkdocs preference changed`);
      let newTheme = getMkdocsThemeState();
      if (newTheme === "auto") {
        newTheme = getThemeState();
      }
      updateTheme(newTheme);
    });
  });
});
