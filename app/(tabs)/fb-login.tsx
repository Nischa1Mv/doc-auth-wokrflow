// app/(tabs)/fb-business-login.tsx
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
  TouchableOpacity,
  View,
} from "react-native";

export default function FBBusinessLoginPage() {
  const [emailOrPhone, setEmailOrPhone] = useState("");
  const [password, setPassword] = useState("");

  const onLogin = () => {
    Alert.alert("Login", "This is a placeholder login action.");
  };

  return (
    <SafeAreaView style={styles.safe}>
      <KeyboardAvoidingView
        style={styles.container}
        behavior={Platform.select({ ios: "padding", android: undefined })}
      >
        <View style={styles.card}>
          <Image
            source={{
              uri: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Meta_Platforms_Inc._logo.svg/512px-Meta_Platforms_Inc._logo.svg.png",
            }}
            style={styles.logo}
            accessibilityLabel="Meta logo"
          />

          <Text style={styles.title}>Log in to Meta Business Suite</Text>

          <View style={styles.inputs}>
            <TextInput
              value={emailOrPhone}
              onChangeText={setEmailOrPhone}
              placeholder="Email or phone number"
              keyboardType="email-address"
              autoCapitalize="none"
              autoCorrect={false}
              style={styles.input}
              placeholderTextColor="#6b7280"
              returnKeyType="next"
            />
            <TextInput
              value={password}
              onChangeText={setPassword}
              placeholder="Password"
              secureTextEntry
              style={styles.input}
              placeholderTextColor="#6b7280"
              returnKeyType="done"
            />
          </View>

          <TouchableOpacity
            onPress={onLogin}
            style={styles.primaryButton}
            activeOpacity={0.9}
            accessibilityRole="button"
            accessibilityLabel="Log In"
          >
            <Text style={styles.primaryButtonText}>Log In</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.linkWrap}
            activeOpacity={0.7}
            accessibilityRole="link"
          >
            <Text style={styles.linkText}>Forgotten password?</Text>
          </TouchableOpacity>

          <View style={styles.dividerRow}>
            <View style={styles.divider} />
            <Text style={styles.orText}>or</Text>
            <View style={styles.divider} />
          </View>

          <TouchableOpacity
            style={styles.secondaryButton}
            activeOpacity={0.9}
            accessibilityRole="button"
            accessibilityLabel="Create new account"
          >
            <Text style={styles.secondaryButtonText}>Create new account</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const BLUE = "#1877F2";

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: "#FFFFFF",
  },
  container: {
    flex: 1,
    backgroundColor: "#FFFFFF",
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 16,
  },
  card: {
    width: "100%",
    maxWidth: 420,
    backgroundColor: "#FFFFFF",
    borderRadius: 12,
    paddingHorizontal: 20,
    paddingVertical: 24,
    ...Platform.select({
      ios: {
        shadowColor: "#000",
        shadowOpacity: 0.08,
        shadowRadius: 12,
        shadowOffset: { width: 0, height: 6 },
      },
      android: {
        elevation: 4,
      },
    }),
  },
  logo: {
    width: 120,
    height: 36,
    resizeMode: "contain",
    alignSelf: "center",
    marginBottom: 12,
  },
  title: {
    fontSize: 20,
    lineHeight: 26,
    fontWeight: "600",
    textAlign: "center",
    color: "#111827",
    marginBottom: 16,
  },
  inputs: {
    gap: 12,
    marginBottom: 12,
  },
  input: {
    height: 48,
    borderWidth: 1,
    borderColor: "#E5E7EB",
    borderRadius: 8,
    paddingHorizontal: 14,
    backgroundColor: "#FFFFFF",
    color: "#111827",
  },
  primaryButton: {
    height: 48,
    borderRadius: 8,
    backgroundColor: BLUE,
    alignItems: "center",
    justifyContent: "center",
  },
  primaryButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
  },
  linkWrap: {
    marginTop: 12,
    alignItems: "center",
  },
  linkText: {
    color: BLUE,
    fontSize: 14,
    fontWeight: "500",
  },
  dividerRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginVertical: 16,
  },
  divider: {
    flex: 1,
    height: 1,
    backgroundColor: "#E5E7EB",
  },
  orText: {
    color: "#6B7280",
    fontSize: 12,
    fontWeight: "500",
  },
  secondaryButton: {
    height: 48,
    borderRadius: 8,
    borderWidth: 1.5,
    borderColor: BLUE,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#FFFFFF",
  },
  secondaryButtonText: {
    color: BLUE,
    fontSize: 16,
    fontWeight: "600",
  },
});
