/**
 * Table Canvas - Data table with sorting TUI
 */

import React, { useState } from 'react';
import { Box, Text, useInput, useApp } from 'ink';

interface TableCanvasProps {
  columns?: string[];
  rows?: Record<string, any>[];
  title?: string;
  onUpdate?: (data: { selectedRow?: number; selectedColumn?: string }) => void;
  onClose?: () => void;
}

export const TableCanvas: React.FC<TableCanvasProps> = ({
  columns = [],
  rows = [],
  title = 'Data Table',
  onUpdate,
  onClose,
}) => {
  const { exit } = useApp();
  const [selectedRow, setSelectedRow] = useState(0);
  const [selectedCol, setSelectedCol] = useState(0);
  const [sortColumn, setSortColumn] = useState<string | null>(null);
  const [sortAsc, setSortAsc] = useState(true);

  // Auto-detect columns if not provided
  const cols = columns.length > 0 ? columns : (rows[0] ? Object.keys(rows[0]) : []);

  // Sort rows
  const sortedRows = [...rows].sort((a, b) => {
    if (!sortColumn) return 0;
    const aVal = a[sortColumn] ?? '';
    const bVal = b[sortColumn] ?? '';
    const cmp = String(aVal).localeCompare(String(bVal), undefined, { numeric: true });
    return sortAsc ? cmp : -cmp;
  });

  useInput((input, key) => {
    if (key.escape) {
      onClose?.();
      exit();
    }
    if (key.upArrow) {
      setSelectedRow(r => Math.max(0, r - 1));
    }
    if (key.downArrow) {
      setSelectedRow(r => Math.min(sortedRows.length - 1, r + 1));
    }
    if (key.leftArrow) {
      setSelectedCol(c => Math.max(0, c - 1));
    }
    if (key.rightArrow) {
      setSelectedCol(c => Math.min(cols.length - 1, c + 1));
    }
    if (input === 's' || key.return) {
      // Toggle sort on current column
      const col = cols[selectedCol];
      if (sortColumn === col) {
        setSortAsc(!sortAsc);
      } else {
        setSortColumn(col);
        setSortAsc(true);
      }
    }
    if (key.return) {
      onUpdate?.({ selectedRow, selectedColumn: cols[selectedCol] });
    }
  });

  // Calculate column widths
  const colWidths = cols.map(col => {
    const headerLen = col.length;
    const maxDataLen = Math.max(...sortedRows.map(r => String(r[col] ?? '').length), 0);
    return Math.min(Math.max(headerLen, maxDataLen) + 2, 25);
  });

  const renderCell = (value: any, colIdx: number, isHeader: boolean, isSelected: boolean) => {
    const width = colWidths[colIdx];
    const text = String(value ?? '').slice(0, width - 1).padEnd(width - 1);
    return (
      <Box key={colIdx} width={width}>
        <Text
          color={isHeader ? 'cyan' : isSelected ? 'black' : 'white'}
          backgroundColor={isSelected ? 'cyan' : undefined}
          bold={isHeader}
        >
          {text}
        </Text>
      </Box>
    );
  };

  return (
    <Box flexDirection="column" borderStyle="round" borderColor="cyan" padding={1}>
      <Box marginBottom={1} justifyContent="space-between">
        <Text bold color="cyan"> {title} </Text>
        <Text color="gray">arrows: navigate | s/Enter: sort | Esc: close</Text>
      </Box>

      {/* Header */}
      <Box borderStyle="single" borderColor="gray">
        {cols.map((col, i) => (
          <Box key={col} width={colWidths[i]}>
            <Text color="cyan" bold>
              {col.slice(0, colWidths[i] - 3).padEnd(colWidths[i] - 3)}
              {sortColumn === col ? (sortAsc ? ' ^' : ' v') : '  '}
            </Text>
          </Box>
        ))}
      </Box>

      {/* Rows */}
      <Box flexDirection="column" maxHeight={15}>
        {sortedRows.length === 0 ? (
          <Text color="gray" dimColor>No data</Text>
        ) : (
          sortedRows.slice(0, 15).map((row, rowIdx) => (
            <Box key={rowIdx}>
              {cols.map((col, colIdx) =>
                renderCell(
                  row[col],
                  colIdx,
                  false,
                  rowIdx === selectedRow && colIdx === selectedCol
                )
              )}
            </Box>
          ))
        )}
      </Box>

      {/* Status */}
      <Box marginTop={1}>
        <Text color="gray" dimColor>
          Row {selectedRow + 1}/{sortedRows.length} |
          Column: {cols[selectedCol]} |
          {sortColumn ? ` Sorted by ${sortColumn} ${sortAsc ? 'ASC' : 'DESC'}` : ' Unsorted'}
        </Text>
      </Box>
    </Box>
  );
};

export default TableCanvas;
