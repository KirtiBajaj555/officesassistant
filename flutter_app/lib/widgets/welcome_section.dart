import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class WelcomeSection extends StatelessWidget {
  final Function(String) onSuggestionTap;

  const WelcomeSection({
    super.key,
    required this.onSuggestionTap,
  });

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final maxWidth = screenWidth > 900 ? 700.0 : screenWidth * 0.9;
    
    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
        child: ConstrainedBox(
          constraints: BoxConstraints(maxWidth: maxWidth),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const SizedBox(height: 20),
              
              // Logo with gradient background
              _buildLogo(),
              
              const SizedBox(height: 24),
              
              // Main title
              ShaderMask(
                shaderCallback: (bounds) => AppTheme.primaryGradient.createShader(bounds),
                child: Text(
                  'Office Assistant',
                  style: Theme.of(context).textTheme.displayLarge?.copyWith(
                    fontSize: 32,
                    fontWeight: FontWeight.w800,
                    color: Colors.white,
                    letterSpacing: -0.5,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
              
              const SizedBox(height: 8),
              
              // Subtitle
              Text(
                'Your intelligent workspace companion',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: AppTheme.mediumGray,
                  fontWeight: FontWeight.w500,
                  fontSize: 15,
                ),
                textAlign: TextAlign.center,
              ),
              
              const SizedBox(height: 32),
              
              // Capability cards in a grid
              _buildCapabilityGrid(context),
              
              const SizedBox(height: 24),
              
              // Suggestion chips
              _buildSuggestionChips(context),
              
              const SizedBox(height: 40),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLogo() {
    return TweenAnimationBuilder<double>(
      duration: const Duration(milliseconds: 800),
      tween: Tween(begin: 0.0, end: 1.0),
      builder: (context, value, child) {
        return Transform.scale(
          scale: 0.8 + (value * 0.2),
          child: Opacity(
            opacity: value,
            child: Container(
              width: 72,
              height: 72,
              decoration: BoxDecoration(
                gradient: AppTheme.primaryGradient,
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(
                    color: AppTheme.primaryBlue.withOpacity(0.25 * value),
                    blurRadius: 24,
                    offset: const Offset(0, 8),
                  ),
                ],
              ),
              child: const Icon(
                Icons.auto_awesome,
                size: 36,
                color: Colors.white,
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildCapabilityGrid(BuildContext context) {
    final capabilities = [
      _CapabilityItem(
        icon: Icons.phone_in_talk_rounded,
        title: 'Smart Calling',
        description: 'AI-powered calls',
        gradient: AppTheme.primaryGradient,
      ),
      _CapabilityItem(
        icon: Icons.email_rounded,
        title: 'Email Management',
        description: 'Organize & respond',
        gradient: const LinearGradient(
          colors: [Color(0xFF10B981), Color(0xFF059669)],
        ),
      ),
      _CapabilityItem(
        icon: Icons.calendar_today_rounded,
        title: 'Schedule & Plan',
        description: 'Manage meetings',
        gradient: AppTheme.accentGradient,
      ),
      _CapabilityItem(
        icon: Icons.analytics_rounded,
        title: 'Data Insights',
        description: 'Analyze & report',
        gradient: const LinearGradient(
          colors: [Color(0xFFF59E0B), Color(0xFFD97706)],
        ),
      ),
    ];

    final screenWidth = MediaQuery.of(context).size.width;
    final crossAxisCount = screenWidth > 600 ? 4 : 2;

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: crossAxisCount,
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
        childAspectRatio: 1.15,
      ),
      itemCount: capabilities.length,
      itemBuilder: (context, index) {
        return _buildCapabilityCard(context, capabilities[index], index);
      },
    );
  }

  Widget _buildCapabilityCard(BuildContext context, _CapabilityItem item, int index) {
    return TweenAnimationBuilder<double>(
      duration: Duration(milliseconds: 500 + (index * 80)),
      tween: Tween(begin: 0.0, end: 1.0),
      curve: Curves.easeOut,
      builder: (context, value, child) {
        return Transform.translate(
          offset: Offset(0, 15 * (1 - value)),
          child: Opacity(
            opacity: value,
            child: child,
          ),
        );
      },
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: AppTheme.darkText.withOpacity(0.04),
              blurRadius: 12,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Material(
          color: Colors.transparent,
          child: InkWell(
            borderRadius: BorderRadius.circular(16),
            onTap: () {
              onSuggestionTap('Tell me about ${item.title.toLowerCase()}');
            },
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      gradient: item.gradient,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Icon(
                      item.icon,
                      color: Colors.white,
                      size: 20,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    item.title,
                    style: const TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w700,
                      color: AppTheme.darkText,
                      height: 1.2,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    item.description,
                    style: TextStyle(
                      fontSize: 11,
                      color: AppTheme.mediumGray.withOpacity(0.85),
                      height: 1.3,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildSuggestionChips(BuildContext context) {
    final suggestions = [
      'What can you do?',
      'Schedule a call',
      'Check emails',
      'Analyze data',
    ];

    return Column(
      children: [
        Text(
          'Quick actions',
          style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.w600,
            color: AppTheme.mediumGray.withOpacity(0.7),
            letterSpacing: 0.5,
          ),
        ),
        const SizedBox(height: 12),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          alignment: WrapAlignment.center,
          children: suggestions.asMap().entries.map((entry) {
            return TweenAnimationBuilder<double>(
              duration: Duration(milliseconds: 700 + (entry.key * 80)),
              tween: Tween(begin: 0.0, end: 1.0),
              curve: Curves.easeOut,
              builder: (context, value, child) {
                return Transform.scale(
                  scale: 0.8 + (value * 0.2),
                  child: Opacity(opacity: value, child: child),
                );
              },
              child: _buildSuggestionChip(context, entry.value),
            );
          }).toList(),
        ),
      ],
    );
  }

  Widget _buildSuggestionChip(BuildContext context, String text) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: () => onSuggestionTap(text),
        borderRadius: BorderRadius.circular(16),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
          decoration: BoxDecoration(
            color: AppTheme.lightBackground,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(
              color: AppTheme.lightGray.withOpacity(0.5),
              width: 1,
            ),
          ),
          child: Text(
            text,
            style: const TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w500,
              color: AppTheme.darkText,
            ),
          ),
        ),
      ),
    );
  }
}

class _CapabilityItem {
  final IconData icon;
  final String title;
  final String description;
  final Gradient gradient;

  _CapabilityItem({
    required this.icon,
    required this.title,
    required this.description,
    required this.gradient,
  });
}

