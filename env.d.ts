declare module "expo-constants" {
  interface ExpoExtra {
    BACKEND_URL: string;
  }

  export interface ExpoConfig {
    extra?: ExpoExtra;
  }

  export interface AppManifest {
    extra?: ExpoExtra;
  }

  const Constants: {
    expoConfig?: ExpoConfig;
    manifest?: AppManifest;
  };

  export default Constants;
}
