import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:intl/intl.dart';
import '../models/message.dart';
import '../theme/app_theme.dart';

class MessageBubble extends StatelessWidget {
  final Message message;
  final bool isAnimating;

  const MessageBubble({
    super.key,
    required this.message,
    this.isAnimating = false,
  });

  @override
  Widget build(BuildContext context) {
    final isUser = message.type == MessageType.user;
    final isSystem = message.type == MessageType.system;
    final isError = message.type == MessageType.error;

    return Padding(
      padding: EdgeInsets.only(
        left: isUser ? 60 : 16,
        right: isUser ? 16 : 60,
        bottom: 12,
      ),
      child: Column(
        crossAxisAlignment:
            isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
        children: [
          if (isSystem)
            _buildSystemMessage()
          else if (isError)
            _buildErrorMessage()
          else
            _buildChatMessage(isUser),
          const SizedBox(height: 4),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12),
            child: Text(
              _formatTimestamp(message.timestamp),
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: AppTheme.mediumGray,
                    fontSize: 11,
                  ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSystemMessage() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppTheme.lightBackground,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: AppTheme.lightGray,
          width: 1,
        ),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              gradient: AppTheme.primaryGradient,
              borderRadius: BorderRadius.circular(8),
            ),
            child: const Icon(
              Icons.info_outline,
              color: Colors.white,
              size: 20,
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              message.content,
              style: const TextStyle(
                color: AppTheme.darkText,
                fontSize: 14,
                height: 1.5,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildErrorMessage() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.red.shade50,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: Colors.red.shade200,
          width: 1,
        ),
      ),
      child: Row(
        children: [
          Icon(
            Icons.error_outline,
            color: Colors.red.shade600,
            size: 20,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              message.content,
              style: TextStyle(
                color: Colors.red.shade900,
                fontSize: 14,
                height: 1.5,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildChatMessage(bool isUser) {
    return GestureDetector(
      onLongPress: () => _showMessageOptions(),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          gradient: isUser ? AppTheme.primaryGradient : null,
          color: isUser ? null : Colors.white,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(20),
            topRight: const Radius.circular(20),
            bottomLeft: Radius.circular(isUser ? 20 : 4),
            bottomRight: Radius.circular(isUser ? 4 : 20),
          ),
          boxShadow: AppTheme.softShadow,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (!isUser) _buildAssistantHeader(),
            SelectableText(
              message.content,
              style: TextStyle(
                color: isUser ? Colors.white : AppTheme.darkText,
                fontSize: 15,
                height: 1.5,
              ),
            ),
            if (message.status == MessageStatus.sending)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: SizedBox(
                  width: 12,
                  height: 12,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    valueColor: AlwaysStoppedAnimation<Color>(
                      isUser ? Colors.white : AppTheme.primaryBlue,
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildAssistantHeader() {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        children: [
          Container(
            width: 24,
            height: 24,
            decoration: BoxDecoration(
              gradient: AppTheme.accentGradient,
              shape: BoxShape.circle,
            ),
            child: const Icon(
              Icons.smart_toy_outlined,
              size: 14,
              color: Colors.white,
            ),
          ),
          const SizedBox(width: 8),
          const Text(
            'Assistant',
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w600,
              color: AppTheme.mediumGray,
            ),
          ),
        ],
      ),
    );
  }

  void _showMessageOptions() {
    // Copy message to clipboard
    Clipboard.setData(ClipboardData(text: message.content));
  }

  String _formatTimestamp(DateTime timestamp) {
    final now = DateTime.now();
    final difference = now.difference(timestamp);

    if (difference.inMinutes < 1) {
      return 'Just now';
    } else if (difference.inHours < 1) {
      return '${difference.inMinutes}m ago';
    } else if (difference.inDays < 1) {
      return DateFormat('HH:mm').format(timestamp);
    } else {
      return DateFormat('MMM d, HH:mm').format(timestamp);
    }
  }
}

