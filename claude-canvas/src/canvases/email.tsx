/**
 * Email Canvas - Interactive email composer TUI
 */

import React, { useState, useEffect } from 'react';
import { Box, Text, useInput, useApp } from 'ink';
import TextInput from 'ink-text-input';

interface EmailData {
  to?: string;
  cc?: string;
  bcc?: string;
  subject?: string;
  body?: string;
}

interface EmailCanvasProps extends EmailData {
  onUpdate?: (data: EmailData) => void;
  onClose?: () => void;
}

type Field = 'to' | 'cc' | 'bcc' | 'subject' | 'body';

export const EmailCanvas: React.FC<EmailCanvasProps> = ({
  to: initialTo = '',
  cc: initialCc = '',
  bcc: initialBcc = '',
  subject: initialSubject = '',
  body: initialBody = '',
  onUpdate,
  onClose,
}) => {
  const { exit } = useApp();
  const [activeField, setActiveField] = useState<Field>('to');
  const [to, setTo] = useState(initialTo);
  const [cc, setCc] = useState(initialCc);
  const [bcc, setBcc] = useState(initialBcc);
  const [subject, setSubject] = useState(initialSubject);
  const [body, setBody] = useState(initialBody);

  const fields: Field[] = ['to', 'cc', 'bcc', 'subject', 'body'];

  useInput((input, key) => {
    if (key.escape) {
      onClose?.();
      exit();
    }
    if (key.tab || (key.return && activeField !== 'body')) {
      const idx = fields.indexOf(activeField);
      setActiveField(fields[(idx + 1) % fields.length]);
    }
    if (key.upArrow) {
      const idx = fields.indexOf(activeField);
      setActiveField(fields[(idx - 1 + fields.length) % fields.length]);
    }
    if (key.downArrow) {
      const idx = fields.indexOf(activeField);
      setActiveField(fields[(idx + 1) % fields.length]);
    }
    // Ctrl+S to send/save
    if (key.ctrl && input === 's') {
      onUpdate?.({ to, cc, bcc, subject, body });
    }
  });

  // Notify on changes
  useEffect(() => {
    const timer = setTimeout(() => {
      onUpdate?.({ to, cc, bcc, subject, body });
    }, 500);
    return () => clearTimeout(timer);
  }, [to, cc, bcc, subject, body]);

  const FieldRow: React.FC<{ label: string; field: Field; value: string; onChange: (v: string) => void }> =
    ({ label, field, value, onChange }) => (
      <Box>
        <Box width={10}>
          <Text color={activeField === field ? 'cyan' : 'gray'} bold={activeField === field}>
            {label}:
          </Text>
        </Box>
        <Box flexGrow={1}>
          {activeField === field ? (
            <TextInput value={value} onChange={onChange} focus={true} />
          ) : (
            <Text color="white">{value || '(empty)'}</Text>
          )}
        </Box>
      </Box>
    );

  return (
    <Box flexDirection="column" borderStyle="round" borderColor="cyan" padding={1}>
      <Box marginBottom={1}>
        <Text bold color="cyan"> Email Composer </Text>
        <Text color="gray"> (Tab: next, Esc: close, Ctrl+S: save)</Text>
      </Box>

      <FieldRow label="To" field="to" value={to} onChange={setTo} />
      <FieldRow label="Cc" field="cc" value={cc} onChange={setCc} />
      <FieldRow label="Bcc" field="bcc" value={bcc} onChange={setBcc} />
      <FieldRow label="Subject" field="subject" value={subject} onChange={setSubject} />

      <Box marginTop={1} flexDirection="column">
        <Text color={activeField === 'body' ? 'cyan' : 'gray'} bold={activeField === 'body'}>
          Body:
        </Text>
        <Box
          borderStyle="single"
          borderColor={activeField === 'body' ? 'cyan' : 'gray'}
          padding={1}
          minHeight={5}
        >
          {activeField === 'body' ? (
            <TextInput value={body} onChange={setBody} focus={true} />
          ) : (
            <Text>{body || '(empty)'}</Text>
          )}
        </Box>
      </Box>

      <Box marginTop={1}>
        <Text color="gray" dimColor>
          Recipients: {[to, cc, bcc].filter(Boolean).length} |
          Subject: {subject.length} chars |
          Body: {body.length} chars
        </Text>
      </Box>
    </Box>
  );
};

export default EmailCanvas;
