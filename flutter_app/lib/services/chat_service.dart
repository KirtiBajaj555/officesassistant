import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart' show kIsWeb;

class ChatService {
  // Auto-detect environment
  static String get baseUrl {
    if (kIsWeb) {
      // Web: Use production URL or localhost for dev
      // For development with local backend:
      return 'http://localhost:8000';
      
      // For production (uncomment when deployed):
      // return 'https://office-agent-backend-xxxxx.run.app';
    } else {
      // Mobile: Android emulator
      return 'http://10.0.2.2:8000';
      // For iOS simulator, use: 'http://localhost:8000'
    }
  }
  
  Future<String> sendMessage({
    required String message,
    required String userId,
    required String accessToken,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/chat'),  // Updated endpoint
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'message': message,
          'user_id': userId,  // Added user_id
          'access_token': accessToken,  // Added access_token
        }),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['response'] ?? 'No response';
      } else {
        return 'Error: ${response.statusCode} - ${response.body}';
      }
    } catch (e) {
      return 'Error: $e';
    }
  }
  
  Future<bool> checkHealth() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/health'));
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
