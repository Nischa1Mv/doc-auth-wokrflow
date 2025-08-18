import { BACKEND_URL } from "@/config";
import { useRouter } from "expo-router";
import React, { useState } from "react";
import {
  Alert,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import { saveToken } from "../utils/storage";

interface LoginResponse {
  access_token: string;
  token_type: string;
}

export default function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

 const handleLogin = async (): Promise<void> => {
  if (!email || !password) {
    Alert.alert("Error", "Please fill all fields");
    return;
  }
  setLoading(true);

  try {
    const res = await fetch(`${BACKEND_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data: LoginResponse = await res.json();
    if (!res.ok) throw new Error((data as any).detail || "Login failed");

    // ✅ use secure storage (AsyncStorage on web, SecureStore on native)
    await saveToken("access_token", data.access_token);
    await saveToken("token_type", data.token_type);

    console.log("Access token:", data.access_token);
    Alert.alert("Success", "Logged in!");
    router.replace("/(protected)");
  } catch (err: any) {
    Alert.alert("Error", err.message || "Login failed");
  } finally {
    setLoading(false);
  }
};

  return (
    <View style={styles.form}>
      <Text style={styles.title}>Step 1: Login to Your Account</Text>
      <Text style={styles.subtitle}>Welcome! Please log in to continue setup.</Text>

      <Text style={styles.label}>Email</Text>
      <TextInput
        style={styles.input}
        placeholder="you@example.com"
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
      />

      <Text style={styles.label}>Password</Text>
      <TextInput
        style={styles.input}
        placeholder="••••••••"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      <TouchableOpacity style={styles.primaryButton} onPress={handleLogin} disabled={loading}>
        <Text style={styles.primaryButtonText}>
          {loading ? "Please wait..." : "Login"}
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const PRIMARY = "#2563EB";

const styles = StyleSheet.create({
  form: { padding: 24 },
  title: { fontSize: 28, fontWeight: "700", textAlign: "center", marginBottom: 8 },
  subtitle: { textAlign: "center", marginBottom: 24, color: "#64748B" },
  label: { marginTop: 12, fontWeight: "600", color: "#0F172A" },
  input: {
    borderWidth: 1,
    borderColor: "#E2E8F0",
    borderRadius: 8,
    padding: 12,
    marginTop: 6,
  },
  primaryButton: {
    backgroundColor: PRIMARY,
    padding: 14,
    borderRadius: 8,
    alignItems: "center",
    marginTop: 24,
  },
  primaryButtonText: { color: "#fff", fontWeight: "600" },
});
