/**
 * JSON Canvas - JSON viewer/explorer TUI
 */

import React, { useState } from 'react';
import { Box, Text, useInput, useApp } from 'ink';

interface JsonCanvasProps {
  data?: any;
  title?: string;
  onUpdate?: (data: { path: string[]; value: any }) => void;
  onClose?: () => void;
}

interface TreeNode {
  key: string;
  value: any;
  path: string[];
  depth: number;
  isExpanded: boolean;
  type: 'object' | 'array' | 'string' | 'number' | 'boolean' | 'null';
}

export const JsonCanvas: React.FC<JsonCanvasProps> = ({
  data = {},
  title = 'JSON Viewer',
  onUpdate,
  onClose,
}) => {
  const { exit } = useApp();
  const [expandedPaths, setExpandedPaths] = useState<Set<string>>(new Set(['']));
  const [selectedIdx, setSelectedIdx] = useState(0);

  const getType = (val: any): TreeNode['type'] => {
    if (val === null) return 'null';
    if (Array.isArray(val)) return 'array';
    return typeof val as TreeNode['type'];
  };

  const flattenTree = (obj: any, path: string[] = [], depth: number = 0): TreeNode[] => {
    const nodes: TreeNode[] = [];
    const pathStr = path.join('.');

    if (typeof obj !== 'object' || obj === null) {
      return nodes;
    }

    const entries = Array.isArray(obj)
      ? obj.map((v, i) => [String(i), v] as [string, any])
      : Object.entries(obj);

    for (const [key, value] of entries) {
      const nodePath = [...path, key];
      const nodePathStr = nodePath.join('.');
      const type = getType(value);
      const isExpandable = type === 'object' || type === 'array';
      const isExpanded = expandedPaths.has(nodePathStr);

      nodes.push({
        key,
        value,
        path: nodePath,
        depth,
        isExpanded,
        type,
      });

      if (isExpandable && isExpanded) {
        nodes.push(...flattenTree(value, nodePath, depth + 1));
      }
    }

    return nodes;
  };

  const nodes = flattenTree(data);

  useInput((input, key) => {
    if (key.escape) {
      onClose?.();
      exit();
    }
    if (key.upArrow) {
      setSelectedIdx(i => Math.max(0, i - 1));
    }
    if (key.downArrow) {
      setSelectedIdx(i => Math.min(nodes.length - 1, i + 1));
    }
    if (key.return || input === ' ') {
      const node = nodes[selectedIdx];
      if (node && (node.type === 'object' || node.type === 'array')) {
        const pathStr = node.path.join('.');
        const newExpanded = new Set(expandedPaths);
        if (newExpanded.has(pathStr)) {
          newExpanded.delete(pathStr);
        } else {
          newExpanded.add(pathStr);
        }
        setExpandedPaths(newExpanded);
      }
    }
    if (key.return) {
      const node = nodes[selectedIdx];
      if (node) {
        onUpdate?.({ path: node.path, value: node.value });
      }
    }
  });

  const getValueColor = (type: TreeNode['type']) => {
    switch (type) {
      case 'string': return 'green';
      case 'number': return 'yellow';
      case 'boolean': return 'magenta';
      case 'null': return 'gray';
      case 'object': return 'cyan';
      case 'array': return 'blue';
      default: return 'white';
    }
  };

  const formatValue = (node: TreeNode): string => {
    const { value, type } = node;
    switch (type) {
      case 'string': return `"${String(value).slice(0, 40)}${String(value).length > 40 ? '...' : ''}"`;
      case 'number': return String(value);
      case 'boolean': return String(value);
      case 'null': return 'null';
      case 'object': return node.isExpanded ? '{' : `{ ${Object.keys(value).length} keys }`;
      case 'array': return node.isExpanded ? '[' : `[ ${value.length} items ]`;
      default: return String(value);
    }
  };

  const renderNode = (node: TreeNode, idx: number) => {
    const indent = '  '.repeat(node.depth);
    const isExpandable = node.type === 'object' || node.type === 'array';
    const arrow = isExpandable ? (node.isExpanded ? '[-]' : '[+]') : '   ';
    const isSelected = idx === selectedIdx;

    return (
      <Box key={node.path.join('.')}>
        <Text
          color={isSelected ? 'black' : 'white'}
          backgroundColor={isSelected ? 'cyan' : undefined}
        >
          {indent}{arrow} </Text>
        <Text
          color={isSelected ? 'black' : 'cyan'}
          backgroundColor={isSelected ? 'cyan' : undefined}
          bold
        >
          {node.key}
        </Text>
        <Text color={isSelected ? 'black' : 'gray'} backgroundColor={isSelected ? 'cyan' : undefined}>: </Text>
        <Text
          color={isSelected ? 'black' : getValueColor(node.type)}
          backgroundColor={isSelected ? 'cyan' : undefined}
        >
          {formatValue(node)}
        </Text>
      </Box>
    );
  };

  return (
    <Box flexDirection="column" borderStyle="round" borderColor="cyan" padding={1}>
      <Box marginBottom={1} justifyContent="space-between">
        <Text bold color="cyan"> {title} </Text>
        <Text color="gray">arrows: navigate | Space/Enter: expand | Esc: close</Text>
      </Box>

      {/* Tree view */}
      <Box flexDirection="column" maxHeight={20}>
        {nodes.length === 0 ? (
          <Text color="gray" dimColor>Empty object</Text>
        ) : (
          nodes.slice(0, 20).map((node, idx) => renderNode(node, idx))
        )}
        {nodes.length > 20 && (
          <Text color="gray" dimColor>... and {nodes.length - 20} more nodes</Text>
        )}
      </Box>

      {/* Status */}
      <Box marginTop={1}>
        <Text color="gray" dimColor>
          Node {selectedIdx + 1}/{nodes.length} |
          Path: {nodes[selectedIdx]?.path.join('.') || 'root'} |
          Type: {nodes[selectedIdx]?.type || 'unknown'}
        </Text>
      </Box>
    </Box>
  );
};

export default JsonCanvas;
