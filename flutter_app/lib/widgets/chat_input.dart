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
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border(
          top: BorderSide(
            color: AppTheme.lightGray.withOpacity(0.5),
            width: 1,
          ),
        ),
      ),
      child: SafeArea(
        top: false,
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            // Attachment button - more refined
            Container(
              margin: const EdgeInsets.only(right: 10, bottom: 2),
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: AppTheme.lightBackground,
                borderRadius: BorderRadius.circular(10),
              ),
              child: IconButton(
                icon: const Icon(Icons.add_rounded),
                onPressed: widget.isEnabled ? _showAttachmentOptions : null,
                color: AppTheme.primaryBlue,
                iconSize: 22,
                padding: EdgeInsets.zero,
              ),
            ),
            
            // Text input - cleaner design
            Expanded(
              child: Container(
                constraints: const BoxConstraints(maxHeight: 120),
                decoration: BoxDecoration(
                  color: AppTheme.lightBackground,
                  borderRadius: BorderRadius.circular(22),
                  border: Border.all(
                    color: _focusNode.hasFocus
                        ? AppTheme.primaryBlue.withOpacity(0.3)
                        : Colors.transparent,
                    width: 1.5,
                  ),
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
                    fontWeight: FontWeight.w400,
                    height: 1.4,
                  ),
                  decoration: InputDecoration(
                    hintText: 'Message Assistant...',
                    hintStyle: TextStyle(
                      color: AppTheme.mediumGray.withOpacity(0.6),
                      fontSize: 15,
                      fontWeight: FontWeight.w400,
                    ),
                    border: InputBorder.none,
                    contentPadding: const EdgeInsets.symmetric(
                      horizontal: 18,
                      vertical: 11,
                    ),
                  ),
                  onSubmitted: (_) => _handleSend(),
                ),
              ),
            ),
            
            const SizedBox(width: 10),
            
            // Send button - premium design
            AnimatedScale(
              scale: _hasText && widget.isEnabled ? 1.0 : 0.9,
              duration: const Duration(milliseconds: 200),
              curve: Curves.easeOut,
              child: Container(
                margin: const EdgeInsets.only(bottom: 2),
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  gradient: _hasText && widget.isEnabled
                      ? AppTheme.primaryGradient
                      : null,
                  color: _hasText && widget.isEnabled
                      ? null
                      : AppTheme.lightGray.withOpacity(0.5),
                  borderRadius: BorderRadius.circular(10),
                  boxShadow: _hasText && widget.isEnabled
                      ? [
                          BoxShadow(
                            color: AppTheme.primaryBlue.withOpacity(0.3),
                            blurRadius: 12,
                            offset: const Offset(0, 4),
                          ),
                        ]
                      : null,
                ),
                child: IconButton(
                  icon: Icon(
                    _hasText ? Icons.arrow_upward_rounded : Icons.arrow_upward_rounded,
                    size: 20,
                  ),
                  onPressed: _hasText && widget.isEnabled ? _handleSend : null,
                  color: Colors.white,
                  padding: EdgeInsets.zero,
                ),
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

