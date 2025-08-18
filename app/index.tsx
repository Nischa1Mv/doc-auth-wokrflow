import { getToken } from "@/utils/storage";
import { Redirect } from "expo-router";
import { useEffect, useState } from "react";
import { ActivityIndicator, View } from "react-native";

export default function Index() {
  const [loading, setLoading] = useState(true);
  const [hasToken, setHasToken] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const token = await getToken("access_token");
        console.log("Index: Checking token:", token);
        const isValid = !!(token && token.trim().length > 0);
        setHasToken(isValid);
        console.log("Index: Has valid token?", isValid);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  console.log("Index: Redirecting to:", hasToken ? "/(protected)" : "/(auth)/login");
  
  if (hasToken) {
    return <Redirect href="/(protected)" />;
  } else {
    return <Redirect href="/(auth)/login" />;
  }
}
