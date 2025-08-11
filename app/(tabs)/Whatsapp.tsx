// app/(tabs)/wa-business-login.tsx
import React, { useState } from "react";
import {
  Alert,
  Image,
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  StyleSheet,
  Text,
  TextInput,
  View,
  Pressable,
} from "react-native";

export default function WABusinessLoginPage() {
  const [phone, setPhone] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const onLogin = () => {
    Alert.alert("Login", "This is a placeholder login action.");
  };

  const onForgotPassword = () => {
    Alert.alert("Forgotten password?", "Password reset flow goes here.");
  };

  const onCreateAccount = () => {
    Alert.alert("Create new account", "Sign up flow goes here.");
  };

  return (
    <SafeAreaView style={styles.screen}>
      <KeyboardAvoidingView
        style={styles.flex}
        behavior={Platform.select({ ios: "padding", android: undefined })}
      >
        <View style={styles.container}>
          <View style={styles.card}>
            <View style={styles.header}>
              <Image
                source={{
                  uri: "https://upload.wikimedia.org/wikipedia/commons/5/5e/WhatsApp_icon.png",
                }}
                resizeMode="contain"
                style={styles.logo}
              />
              <Text style={styles.title}>Log in to WhatsApp Business</Text>
            </View>

            <View style={styles.form}>
              <TextInput
                value={phone}
                onChangeText={setPhone}
                placeholder="Phone number"
                keyboardType="phone-pad"
                textContentType="telephoneNumber"
                autoComplete="tel"
                style={styles.input}
                placeholderTextColor="#6b7280"
              />

              <TextInput
                value={password}
                onChangeText={setPassword}
                placeholder="Password"
                secureTextEntry
                textContentType="password"
                autoComplete="password"
                style={styles.input}
                placeholderTextColor="#6b7280"
              />

              <Pressable
                onPress={onLogin}
                android_ripple={{ color: "rgba(255,255,255,0.15)" }}
                style={({ pressed }) => [
                  styles.primaryButton,
                  pressed && styles.primaryPressed,
                ]}
              >
                <Text style={styles.primaryButtonText}>Log In</Text>
              </Pressable>

              <Pressable onPress={onForgotPassword} style={styles.linkWrap}>
                <Text style={styles.link}>Forgotten password?</Text>
              </Pressable>

              <View style={styles.divider}>
                <View style={styles.line} />
                <Text style={styles.orText}>or</Text>
                <View style={styles.line} />
              </View>

              <Pressable
                onPress={onCreateAccount}
                style={({ pressed }) => [
                  styles.secondaryButton,
                  pressed && styles.secondaryPressed,
                ]}
              >
                <Text style={styles.secondaryButtonText}>
                  Create new account
                </Text>
              </Pressable>
            </View>
          </View>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const WA_GREEN = "#25D366";

const styles = StyleSheet.create({
  flex: { flex: 1 },
  screen: {
    flex: 1,
    backgroundColor: "#FFFFFF",
  },
  container: {
    flex: 1,
    paddingHorizontal: 16,
    justifyContent: "center",
    alignItems: "center",
  },
  card: {
    width: "100%",
    maxWidth: 440,
    backgroundColor: "#FFFFFF",
    borderRadius: 14,
    padding: 24,
    // iOS shadow
    shadowColor: "#000",
    shadowOpacity: 0.08,
    shadowRadius: 16,
    shadowOffset: { width: 0, height: 6 },
    // Android elevation
    elevation: 6,
  },
  header: {
    alignItems: "center",
    marginBottom: 16,
  },
  logo: {
    width: 56,
    height: 56,
    marginBottom: 12,
  },
  title: {
    fontSize: 20,
    lineHeight: 28,
    fontWeight: "700",
    color: "#0f172a",
    textAlign: "center",
  },
  form: {
    marginTop: 8,
  },
  input: {
    height: 48,
    borderWidth: 1,
    borderColor: "#e5e7eb",
    borderRadius: 10,
    paddingHorizontal: 12,
    color: "#0f172a",
    backgroundColor: "#FFFFFF",
    marginBottom: 12,
  },
  primaryButton: {
    height: 48,
    borderRadius: 10,
    backgroundColor: WA_GREEN,
    alignItems: "center",
    justifyContent: "center",
  },
  primaryPressed: {
    opacity: 0.95,
  },
  primaryButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },
  linkWrap: {
    marginTop: 12,
    alignItems: "center",
  },
  link: {
    color: WA_GREEN,
    fontSize: 14,
    fontWeight: "600",
  },
  divider: {
    flexDirection: "row",
    alignItems: "center",
    marginVertical: 16,
  },
  line: {
    flex: 1,
    height: 1,
    backgroundColor: "#e5e7eb",
  },
  orText: {
    marginHorizontal: 12,
    color: "#6b7280",
    fontSize: 13,
    fontWeight: "600",
  },
  secondaryButton: {
    height: 48,
    borderRadius: 10,
    borderWidth: 1.5,
    borderColor: WA_GREEN,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#FFFFFF",
  },
  secondaryPressed: {
    opacity: 0.9,
  },
  secondaryButtonText: {
    color: WA_GREEN,
    fontSize: 16,
    fontWeight: "700",
  },
});
