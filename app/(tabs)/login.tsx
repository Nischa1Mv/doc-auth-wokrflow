import React, { useState } from "react";
import { SafeAreaView, TouchableOpacity, Text, StyleSheet } from "react-native";
import Animated, {
  FadeInRight,
  FadeOutLeft,
} from "react-native-reanimated";

import LoginForm from "../../components/LoginForm";
import SignupForm from "../../components/SignupForm";

export default function AuthScreen() {
  const [isLogin, setIsLogin] = useState<boolean>(true);

  return (
    <SafeAreaView style={styles.container}>
      <Animated.View
        key={isLogin ? "login" : "signup"} // force re-render for animation
        entering={FadeInRight.duration(300)}
        exiting={FadeOutLeft.duration(300)}
        style={{ flex: 1, justifyContent: "center" }}
      >
        {isLogin ? <LoginForm /> : <SignupForm />}
      </Animated.View>

      <TouchableOpacity
        style={styles.linkButton}
        onPress={() => setIsLogin(!isLogin)}
      >
        <Text style={styles.linkText}>
          {isLogin
            ? "Don’t have an account? Sign Up"
            : "Already have an account? Login"}
        </Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}

const PRIMARY = "#2563EB";

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#fff", padding: 16 },
  linkButton: { marginTop: 16, alignItems: "center" },
  linkText: { color: PRIMARY, fontWeight: "600" },
});
