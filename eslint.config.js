import globals from "globals";
import js from "@eslint/js";

export default [
  js.configs.recommended,
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        Chart: "readonly",
        pannellum: "readonly",
        getAIRecommendations: "readonly",
        gtag: "readonly",
        openModal: "writable",
        libpannellum: "readonly",
        d: "writable",
        u: "writable",
        x: "writable",
        c: "writable",
        n: "writable",
        f: "writable",
        a: "writable",
        g: "writable",
        m: "writable",
        e: "writable",
        h: "writable"
      }
    },
    rules: {
      "no-prototype-builtins": "off",
      "no-cond-assign": "warn",
      "no-redeclare": "warn",
      "no-unused-vars": "warn",
      "no-undef": "error"
    }
  }
];