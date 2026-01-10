/**
 * Todo Canvas - Interactive todo list TUI
 */

import React, { useState } from 'react';
import { Box, Text, useInput, useApp } from 'ink';
import TextInput from 'ink-text-input';

interface TodoItem {
  id: string;
  text: string;
  done: boolean;
  priority?: 'high' | 'medium' | 'low';
}

interface TodoCanvasProps {
  title?: string;
  items?: TodoItem[];
  onUpdate?: (data: { items: TodoItem[] }) => void;
  onClose?: () => void;
}

export const TodoCanvas: React.FC<TodoCanvasProps> = ({
  title = 'Todo List',
  items: initialItems = [],
  onUpdate,
  onClose,
}) => {
  const { exit } = useApp();
  // Ensure all items have IDs
  const [items, setItems] = useState<TodoItem[]>(
    initialItems.map((item, idx) => ({
      ...item,
      id: item.id || `todo_${Date.now()}_${idx}`,
    }))
  );
  const [selectedIdx, setSelectedIdx] = useState(0);
  const [isAdding, setIsAdding] = useState(false);
  const [newItemText, setNewItemText] = useState('');

  const updateItems = (newItems: TodoItem[]) => {
    setItems(newItems);
    onUpdate?.({ items: newItems });
  };

  useInput((input, key) => {
    if (isAdding) {
      if (key.escape) {
        setIsAdding(false);
        setNewItemText('');
      }
      if (key.return && newItemText.trim()) {
        const newItem: TodoItem = {
          id: `todo_${Date.now()}`,
          text: newItemText.trim(),
          done: false,
        };
        updateItems([...items, newItem]);
        setNewItemText('');
        setIsAdding(false);
        setSelectedIdx(items.length);
      }
      return;
    }

    if (key.escape) {
      onClose?.();
      exit();
    }
    if (key.upArrow) {
      setSelectedIdx(i => Math.max(0, i - 1));
    }
    if (key.downArrow) {
      setSelectedIdx(i => Math.min(items.length - 1, i + 1));
    }
    if (input === ' ' || key.return) {
      // Toggle done
      if (items[selectedIdx]) {
        const newItems = [...items];
        newItems[selectedIdx] = { ...newItems[selectedIdx], done: !newItems[selectedIdx].done };
        updateItems(newItems);
      }
    }
    if (input === 'a' || input === 'n') {
      setIsAdding(true);
    }
    if (input === 'd' || key.delete) {
      // Delete item
      if (items[selectedIdx]) {
        const newItems = items.filter((_, i) => i !== selectedIdx);
        updateItems(newItems);
        setSelectedIdx(Math.min(selectedIdx, newItems.length - 1));
      }
    }
    if (input === '1') {
      // Set high priority
      if (items[selectedIdx]) {
        const newItems = [...items];
        newItems[selectedIdx] = { ...newItems[selectedIdx], priority: 'high' };
        updateItems(newItems);
      }
    }
    if (input === '2') {
      // Set medium priority
      if (items[selectedIdx]) {
        const newItems = [...items];
        newItems[selectedIdx] = { ...newItems[selectedIdx], priority: 'medium' };
        updateItems(newItems);
      }
    }
    if (input === '3') {
      // Set low priority
      if (items[selectedIdx]) {
        const newItems = [...items];
        newItems[selectedIdx] = { ...newItems[selectedIdx], priority: 'low' };
        updateItems(newItems);
      }
    }
  });

  const getPriorityColor = (priority?: string) => {
    switch (priority) {
      case 'high': return 'red';
      case 'medium': return 'yellow';
      case 'low': return 'blue';
      default: return 'gray';
    }
  };

  const getPriorityIndicator = (priority?: string) => {
    switch (priority) {
      case 'high': return '!!!';
      case 'medium': return '!! ';
      case 'low': return '!  ';
      default: return '   ';
    }
  };

  const doneCount = items.filter(i => i.done).length;

  return (
    <Box flexDirection="column" borderStyle="round" borderColor="cyan" padding={1}>
      <Box marginBottom={1} justifyContent="space-between">
        <Text bold color="cyan"> {title} </Text>
        <Text color="gray">Space: toggle | a: add | d: delete | 1/2/3: priority</Text>
      </Box>

      {/* Progress bar */}
      <Box marginBottom={1}>
        <Text color="gray">[</Text>
        <Text color="green">{'='.repeat(Math.floor((doneCount / Math.max(items.length, 1)) * 20))}</Text>
        <Text color="gray">{' '.repeat(20 - Math.floor((doneCount / Math.max(items.length, 1)) * 20))}</Text>
        <Text color="gray">] {doneCount}/{items.length}</Text>
      </Box>

      {/* Items */}
      <Box flexDirection="column" maxHeight={15}>
        {items.length === 0 && !isAdding ? (
          <Text color="gray" dimColor>No items. Press 'a' to add.</Text>
        ) : (
          items.map((item, idx) => (
            <Box key={item.id}>
              <Text
                color={idx === selectedIdx ? 'black' : item.done ? 'gray' : 'white'}
                backgroundColor={idx === selectedIdx ? 'cyan' : undefined}
                strikethrough={item.done}
                dimColor={item.done}
              >
                {item.done ? '[x]' : '[ ]'} {' '}
              </Text>
              <Text color={getPriorityColor(item.priority)}>{getPriorityIndicator(item.priority)}</Text>
              <Text
                color={idx === selectedIdx ? 'black' : item.done ? 'gray' : 'white'}
                backgroundColor={idx === selectedIdx ? 'cyan' : undefined}
                strikethrough={item.done}
                dimColor={item.done}
              >
                {item.text}
              </Text>
            </Box>
          ))
        )}

        {/* Add new item input */}
        {isAdding && (
          <Box>
            <Text color="green">[+] </Text>
            <TextInput
              value={newItemText}
              onChange={setNewItemText}
              placeholder="Enter new item..."
              focus={true}
            />
          </Box>
        )}
      </Box>

      {/* Status */}
      <Box marginTop={1}>
        <Text color="gray" dimColor>
          {items.length} items | {doneCount} completed | {items.length - doneCount} remaining
        </Text>
      </Box>
    </Box>
  );
};

export default TodoCanvas;
