import { deleteToken } from "@/utils/storage";
import { router } from "expo-router";
import { SafeAreaView, Text, TouchableOpacity } from "react-native";

export default function Home() {
  const signOut = async () => {
    await Promise.all([
      deleteToken("access_token"),
      deleteToken("token_type"),
    ]);
    router.replace("(auth)/login");
  };

  return (
    <SafeAreaView style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text style={{ fontSize: 24, fontWeight: "bold" }}>You're in ✅</Text>
      <Text>Next step: Connect WhatsApp</Text>

      <TouchableOpacity
        style={{ marginTop: 20, padding: 14, backgroundColor: "red", borderRadius: 8 }}
        onPress={signOut}
      >
        <Text style={{ color: "white" }}>Sign out</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}
