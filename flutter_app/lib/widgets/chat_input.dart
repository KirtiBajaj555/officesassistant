import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class ChatInput extends StatefulWidget {
  final Function(String) onSendMessage;
  final bool isEnabled;

  const ChatInput({
    super.key,
    required this.onSendMessage,
    this.isEnabled = true,
  });

  @override
  State<ChatInput> createState() => _ChatInputState();
}

class _ChatInputState extends State<ChatInput> {
  final TextEditingController _controller = TextEditingController();
  final FocusNode _focusNode = FocusNode();
  bool _hasText = false;

  @override
  void initState() {
    super.initState();
    _controller.addListener(_onTextChanged);
  }

  @override
  void dispose() {
    _controller.dispose();
    _focusNode.dispose();
    super.dispose();
  }

  void _onTextChanged() {
    setState(() {
      _hasText = _controller.text.trim().isNotEmpty;
    });
  }

  void _handleSend() {
    if (_hasText && widget.isEnabled) {
      widget.onSendMessage(_controller.text.trim());
      _controller.clear();
      _focusNode.requestFocus();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: AppTheme.darkText.withOpacity(0.05),
            blurRadius: 20,
            offset: const Offset(0, -4),
          ),
        ],
      ),
      child: SafeArea(
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            // Attachment button
            Container(
              margin: const EdgeInsets.only(right: 8, bottom: 4),
              decoration: BoxDecoration(
                color: AppTheme.lightBackground,
                borderRadius: BorderRadius.circular(12),
              ),
              child: IconButton(
                icon: const Icon(Icons.add_circle_outline),
                onPressed: widget.isEnabled ? _showAttachmentOptions : null,
                color: AppTheme.primaryBlue,
                iconSize: 26,
              ),
            ),
            
            // Text input
            Expanded(
              child: Container(
                constraints: const BoxConstraints(maxHeight: 120),
                decoration: BoxDecoration(
                  color: AppTheme.lightBackground,
                  borderRadius: BorderRadius.circular(24),
                ),
                child: TextField(
                  controller: _controller,
                  focusNode: _focusNode,
                  enabled: widget.isEnabled,
                  maxLines: null,
                  textInputAction: TextInputAction.newline,
                  style: const TextStyle(
                    fontSize: 15,
                    color: AppTheme.darkText,
                  ),
                  decoration: InputDecoration(
                    hintText: 'Ask me anything...',
                    hintStyle: TextStyle(
                      color: AppTheme.mediumGray.withOpacity(0.7),
                      fontSize: 15,
                    ),
                    border: InputBorder.none,
                    contentPadding: const EdgeInsets.symmetric(
                      horizontal: 20,
                      vertical: 12,
                    ),
                  ),
                  onSubmitted: (_) => _handleSend(),
                ),
              ),
            ),
            
            const SizedBox(width: 8),
            
            // Send button
            AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              margin: const EdgeInsets.only(bottom: 4),
              decoration: BoxDecoration(
                gradient: _hasText && widget.isEnabled
                    ? AppTheme.primaryGradient
                    : null,
                color: _hasText && widget.isEnabled
                    ? null
                    : AppTheme.lightGray,
                borderRadius: BorderRadius.circular(12),
                boxShadow: _hasText && widget.isEnabled
                    ? AppTheme.glowShadow
                    : null,
              ),
              child: IconButton(
                icon: const Icon(Icons.send_rounded),
                onPressed: _hasText && widget.isEnabled ? _handleSend : null,
                color: Colors.white,
                iconSize: 22,
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showAttachmentOptions() {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (context) => Container(
        decoration: const BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
        ),
        padding: const EdgeInsets.symmetric(vertical: 24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 40,
              height: 4,
              decoration: BoxDecoration(
                color: AppTheme.lightGray,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            const SizedBox(height: 24),
            _buildOptionTile(
              icon: Icons.phone,
              title: 'Make a Call',
              subtitle: 'Initiate a phone call',
              gradient: AppTheme.primaryGradient,
              onTap: () {
                Navigator.pop(context);
                _showPhoneCallDialog();
              },
            ),
            _buildOptionTile(
              icon: Icons.attach_file,
              title: 'Attach File',
              subtitle: 'Upload documents',
              gradient: AppTheme.accentGradient,
              onTap: () {
                Navigator.pop(context);
                // Handle file attachment
              },
            ),
            _buildOptionTile(
              icon: Icons.image,
              title: 'Send Image',
              subtitle: 'Share photos',
              gradient: const LinearGradient(
                colors: [AppTheme.successGreen, Color(0xFF059669)],
              ),
              onTap: () {
                Navigator.pop(context);
                // Handle image
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildOptionTile({
    required IconData icon,
    required String title,
    required String subtitle,
    required Gradient gradient,
    required VoidCallback onTap,
  }) {
    return ListTile(
      leading: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          gradient: gradient,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Icon(icon, color: Colors.white, size: 24),
      ),
      title: Text(
        title,
        style: const TextStyle(
          fontWeight: FontWeight.w600,
          color: AppTheme.darkText,
        ),
      ),
      subtitle: Text(
        subtitle,
        style: const TextStyle(
          color: AppTheme.mediumGray,
          fontSize: 13,
        ),
      ),
      onTap: onTap,
    );
  }

  void _showPhoneCallDialog() {
    final phoneController = TextEditingController();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: const Text('Make a Call'),
        content: TextField(
          controller: phoneController,
          keyboardType: TextInputType.phone,
          decoration: const InputDecoration(
            hintText: '+1 234 567 8900',
            prefixIcon: Icon(Icons.phone),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
              widget.onSendMessage('Make a call to ${phoneController.text}');
            },
            child: const Text('Call'),
          ),
        ],
      ),
    );
  }
}

