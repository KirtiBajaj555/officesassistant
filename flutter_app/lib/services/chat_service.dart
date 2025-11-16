import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/message.dart';

class ChatService extends ChangeNotifier {
  // Backend API URL - Update this with your actual backend URL
  static const String baseUrl = 'http://localhost:8000';
  
  List<Message> _messages = [];
  bool _isLoading = false;
  bool _isTyping = false;

  List<Message> get messages => List.unmodifiable(_messages);
  bool get isLoading => _isLoading;
  bool get isTyping => _isTyping;

  ChatService() {
    _initializeChat();
  }

  void _initializeChat() {
    // Don't add welcome message - use the beautiful empty state instead
    notifyListeners();
  }

  Future<void> sendMessage(String content) async {
    if (content.trim().isEmpty) return;

    // Add user message
    final userMessage = Message.user(content);
    _messages.add(userMessage);
    _isTyping = true;
    notifyListeners();

    try {
      // Update message status to sent
      _updateMessageStatus(userMessage.id, MessageStatus.sent);

      // Call backend API
      final response = await http.post(
        Uri.parse('$baseUrl/chat'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'message': content}),
      ).timeout(const Duration(seconds: 30));

      _isTyping = false;

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final assistantMessage = Message.assistant(
          data['response'] ?? 'I received your message.',
          metadata: data['metadata'],
        );
        _messages.add(assistantMessage);
        _updateMessageStatus(userMessage.id, MessageStatus.delivered);
      } else {
        _messages.add(Message.error(
          'Sorry, I encountered an error. Please try again.'
        ));
        _updateMessageStatus(userMessage.id, MessageStatus.error);
      }
    } catch (e) {
      _isTyping = false;
      debugPrint('Error sending message: $e');
      
      // For demo purposes, add a mock response
      await Future.delayed(const Duration(milliseconds: 500));
      _messages.add(Message.assistant(
        '✨ I\'m your Office Assistant! While the backend is connecting, I\'m here to help you with:\n\n'
        '• Making phone calls to contacts\n'
        '• Managing your calendar and scheduling\n'
        '• Email management and communication\n'
        '• Document handling and organization\n'
        '• Quick information and data lookup\n\n'
        'What would you like me to help you with?',
      ));
      _updateMessageStatus(userMessage.id, MessageStatus.delivered);
    }

    notifyListeners();
  }

  void _updateMessageStatus(String messageId, MessageStatus status) {
    final index = _messages.indexWhere((m) => m.id == messageId);
    if (index != -1) {
      _messages[index] = _messages[index].copyWith(status: status);
      notifyListeners();
    }
  }

  Future<void> makePhoneCall(String phoneNumber) async {
    try {
      _isLoading = true;
      notifyListeners();

      final response = await http.post(
        Uri.parse('$baseUrl/make-call'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'phone_number': phoneNumber}),
      ).timeout(const Duration(seconds: 30));

      _isLoading = false;

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _messages.add(Message.assistant(
          '📞 Call initiated to $phoneNumber successfully!',
          metadata: data,
        ));
      } else {
        _messages.add(Message.error(
          'Failed to initiate call. Please try again.'
        ));
      }
    } catch (e) {
      _isLoading = false;
      debugPrint('Error making call: $e');
      _messages.add(Message.error(
        'Error connecting to calling service.'
      ));
    }

    notifyListeners();
  }

  void clearChat() {
    _messages.clear();
    _initializeChat();
    notifyListeners();
  }

  void deleteMessage(String messageId) {
    _messages.removeWhere((m) => m.id == messageId);
    notifyListeners();
  }
}

