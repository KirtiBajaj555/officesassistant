# Assets Directory

## App Icon

To create a custom app icon:

1. **Create your icon image** (1024x1024 px recommended)
   - Use the color scheme: Blue (#2563EB) and Purple (#8B5CF6)
   - Design a modern, minimalist icon
   - Suggested elements: Chat bubble, assistant robot, or stylized "OA" letters

2. **Save as**: `assets/images/icon.png`

3. **Generate platform icons**:
   ```bash
   flutter pub add flutter_launcher_icons
   flutter pub run flutter_launcher_icons
   ```

## Placeholder Icon Design

**Suggested Icon Concept:**
- Background: Gradient from blue to purple
- Foreground: White chat bubble with sparkle/star
- Style: Rounded square with modern feel
- Text: Optional "OA" monogram

You can use tools like:
- Figma: https://figma.com
- Canva: https://canva.com
- Adobe Illustrator
- Or AI image generators with prompt: "Modern office assistant app icon, blue purple gradient, chat bubble, minimalist, professional"

## Other Assets

You can add:
- `assets/images/` - For images and illustrations
- `assets/fonts/` - For custom fonts (if needed)
- `assets/lottie/` - For Lottie animations

## Adding Assets

1. Add files to appropriate folders
2. Update `pubspec.yaml`:
   ```yaml
   flutter:
     assets:
       - assets/images/
       - assets/fonts/
   ```
3. Run `flutter pub get`

