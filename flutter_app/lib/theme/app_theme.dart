import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  // Modern Professional Color Palette
  static const primaryBlue = Color(0xFF2563EB);
  static const deepPurple = Color(0xFF8B5CF6);
  static const hotPink = Color(0xFFEC4899);
  static const lightBackground = Color(0xFFF8FAFC);
  static const darkText = Color(0xFF1E293B);
  static const mediumGray = Color(0xFF64748B);
  static const lightGray = Color(0xFFE2E8F0);
  static const white = Color(0xFFFFFFFF);
  static const successGreen = Color(0xFF10B981);
  static const warningOrange = Color(0xFFF59E0B);
  
  // Beautiful Gradients
  static const primaryGradient = LinearGradient(
    colors: [primaryBlue, deepPurple],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
  
  static const accentGradient = LinearGradient(
    colors: [deepPurple, hotPink],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
  
  static const backgroundGradient = LinearGradient(
    colors: [Color(0xFFF8FAFC), Color(0xFFEEF2FF), Color(0xFFFCF7FF)],
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
  );

  static const shimmerGradient = LinearGradient(
    colors: [
      Color(0xFFE2E8F0),
      Color(0xFFF1F5F9),
      Color(0xFFE2E8F0),
    ],
    stops: [0.1, 0.5, 0.9],
    begin: Alignment(-1.0, -0.5),
    end: Alignment(1.0, 0.5),
  );

  static ThemeData lightTheme = ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
    colorScheme: ColorScheme.light(
      primary: primaryBlue,
      secondary: deepPurple,
      tertiary: hotPink,
      surface: white,
      background: lightBackground,
      onPrimary: white,
      onSurface: darkText,
    ),
    scaffoldBackgroundColor: lightBackground,
    textTheme: GoogleFonts.interTextTheme(
      const TextTheme(
        displayLarge: TextStyle(
          fontSize: 32,
          fontWeight: FontWeight.bold,
          color: darkText,
          letterSpacing: -0.5,
        ),
        displayMedium: TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.w600,
          color: darkText,
        ),
        titleLarge: TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.w600,
          color: darkText,
        ),
        bodyLarge: TextStyle(
          fontSize: 16,
          color: darkText,
          height: 1.5,
        ),
        bodyMedium: TextStyle(
          fontSize: 14,
          color: mediumGray,
          height: 1.5,
        ),
        labelLarge: TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.w600,
          color: white,
        ),
      ),
    ),
    cardTheme: CardThemeData(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
      ),
      color: white,
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        elevation: 0,
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
        backgroundColor: primaryBlue,
        foregroundColor: white,
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: white,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(24),
        borderSide: BorderSide.none,
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(24),
        borderSide: BorderSide.none,
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(24),
        borderSide: const BorderSide(color: primaryBlue, width: 2),
      ),
      contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      hintStyle: const TextStyle(color: mediumGray),
    ),
    iconTheme: const IconThemeData(
      color: mediumGray,
      size: 24,
    ),
  );

  // Box Shadows
  static List<BoxShadow> get softShadow => [
        BoxShadow(
          color: darkText.withOpacity(0.05),
          blurRadius: 20,
          offset: const Offset(0, 4),
        ),
      ];

  static List<BoxShadow> get mediumShadow => [
        BoxShadow(
          color: darkText.withOpacity(0.1),
          blurRadius: 30,
          offset: const Offset(0, 8),
        ),
      ];

  static List<BoxShadow> get glowShadow => [
        BoxShadow(
          color: primaryBlue.withOpacity(0.3),
          blurRadius: 20,
          offset: const Offset(0, 4),
        ),
      ];
}

