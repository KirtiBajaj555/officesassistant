enum MessageType { user, assistant, system, error }

enum MessageStatus { sending, sent, delivered, error }

class Message {
  final String id;
  final String content;
  final MessageType type;
  final DateTime timestamp;
  final MessageStatus status;
  final Map<String, dynamic>? metadata;

  Message({
    required this.id,
    required this.content,
    required this.type,
    required this.timestamp,
    this.status = MessageStatus.delivered,
    this.metadata,
  });

  factory Message.user(String content) {
    return Message(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      content: content,
      type: MessageType.user,
      timestamp: DateTime.now(),
      status: MessageStatus.sending,
    );
  }

  factory Message.assistant(String content, {Map<String, dynamic>? metadata}) {
    return Message(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      content: content,
      type: MessageType.assistant,
      timestamp: DateTime.now(),
      metadata: metadata,
    );
  }

  factory Message.system(String content) {
    return Message(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      content: content,
      type: MessageType.system,
      timestamp: DateTime.now(),
    );
  }

  factory Message.error(String content) {
    return Message(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      content: content,
      type: MessageType.error,
      timestamp: DateTime.now(),
      status: MessageStatus.error,
    );
  }

  Message copyWith({
    String? id,
    String? content,
    MessageType? type,
    DateTime? timestamp,
    MessageStatus? status,
    Map<String, dynamic>? metadata,
  }) {
    return Message(
      id: id ?? this.id,
      content: content ?? this.content,
      type: type ?? this.type,
      timestamp: timestamp ?? this.timestamp,
      status: status ?? this.status,
      metadata: metadata ?? this.metadata,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'content': content,
      'type': type.toString(),
      'timestamp': timestamp.toIso8601String(),
      'status': status.toString(),
      'metadata': metadata,
    };
  }

  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
      id: json['id'],
      content: json['content'],
      type: MessageType.values.firstWhere(
        (e) => e.toString() == json['type'],
        orElse: () => MessageType.assistant,
      ),
      timestamp: DateTime.parse(json['timestamp']),
      status: json['status'] != null
          ? MessageStatus.values.firstWhere(
              (e) => e.toString() == json['status'],
              orElse: () => MessageStatus.delivered,
            )
          : MessageStatus.delivered,
      metadata: json['metadata'],
    );
  }
}

