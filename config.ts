import Constants from "expo-constants";

const extra = Constants.expoConfig?.extra || Constants.manifest?.extra;

export const BACKEND_URL = extra?.BACKEND_URL;
