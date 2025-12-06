import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter/foundation.dart' show kIsWeb;

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  
  // Get current user
  User? get currentUser => _auth.currentUser;
  
  // Sign in with Google - Multi-step approach
  Future<Map<String, dynamic>?> signInWithGoogle() async {
    try {
      if (kIsWeb) {
        // Create Google Auth Provider
        final GoogleAuthProvider googleProvider = GoogleAuthProvider();
        
        // Add scopes for Gmail and Calendar
        googleProvider.addScope('https://www.googleapis.com/auth/gmail.modify');
        googleProvider.addScope('https://www.googleapis.com/auth/calendar');
        
        UserCredential? userCredential;
        
        // Start with account picker to avoid cookie blocking issues
        // (Silent sign-in doesn't work on localhost due to third-party cookie blocking)
        try {
          print('Showing account picker...');
          googleProvider.setCustomParameters({
            'prompt': 'select_account', // Show account picker
          });
          
          userCredential = await _auth.signInWithPopup(googleProvider);
          print('Account picker sign-in successful!');
        } catch (pickerError) {
          print('Account picker failed: $pickerError');
          
          // Fallback: Show full consent screen
          print('Showing full consent screen...');
          googleProvider.setCustomParameters({
            'prompt': 'consent', // Show full consent with email field
          });
          
          userCredential = await _auth.signInWithPopup(googleProvider);
          print('Full consent sign-in successful!');
        }
        
        if (userCredential == null) {
          return null;
        }
        
        // Get access token from credential
        final credential = userCredential.credential as OAuthCredential?;
        final accessToken = credential?.accessToken;
        
        // Store token securely
        if (accessToken != null) {
          await _storage.write(
            key: 'google_access_token',
            value: accessToken,
          );
        }
        
        return {
          'user': userCredential.user,
          'accessToken': accessToken,
          'email': userCredential.user?.email,
          'displayName': userCredential.user?.displayName,
          'photoUrl': userCredential.user?.photoURL,
        };
      } else {
        // Mobile: Not implemented yet
        throw UnimplementedError('Mobile sign-in not implemented yet');
      }
    } catch (e) {
      print('Error signing in: $e');
      return null;
    }
  }
  
  // Get stored access token
  Future<String?> getAccessToken() async {
    return await _storage.read(key: 'google_access_token');
  }
  
  // Sign out
  Future<void> signOut() async {
    await _auth.signOut();
    await _storage.delete(key: 'google_access_token');
  }
  
  // Check if user is signed in
  bool isSignedIn() {
    return _auth.currentUser != null;
  }
}
