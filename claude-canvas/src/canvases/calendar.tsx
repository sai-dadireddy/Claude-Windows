/**
 * Calendar Canvas - Interactive calendar/schedule viewer TUI
 */

import React, { useState } from 'react';
import { Box, Text, useInput, useApp } from 'ink';

interface Event {
  id: string;
  title: string;
  start: string; // ISO date or "HH:MM"
  end?: string;
  color?: string;
}

interface CalendarCanvasProps {
  date?: string; // YYYY-MM-DD
  events?: Event[];
  onUpdate?: (data: { selectedDate?: string; selectedEvent?: Event }) => void;
  onClose?: () => void;
}

const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'];

export const CalendarCanvas: React.FC<CalendarCanvasProps> = ({
  date: initialDate,
  events = [],
  onUpdate,
  onClose,
}) => {
  const { exit } = useApp();
  const today = new Date();
  const [viewDate, setViewDate] = useState(initialDate ? new Date(initialDate) : today);
  const [selectedDay, setSelectedDay] = useState(today.getDate());

  const year = viewDate.getFullYear();
  const month = viewDate.getMonth();
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  useInput((input, key) => {
    if (key.escape) {
      onClose?.();
      exit();
    }
    if (key.leftArrow) {
      setSelectedDay(d => Math.max(1, d - 1));
    }
    if (key.rightArrow) {
      setSelectedDay(d => Math.min(daysInMonth, d + 1));
    }
    if (key.upArrow) {
      setSelectedDay(d => Math.max(1, d - 7));
    }
    if (key.downArrow) {
      setSelectedDay(d => Math.min(daysInMonth, d + 7));
    }
    if (input === '[' || input === 'h') {
      setViewDate(new Date(year, month - 1, 1));
      setSelectedDay(1);
    }
    if (input === ']' || input === 'l') {
      setViewDate(new Date(year, month + 1, 1));
      setSelectedDay(1);
    }
    if (key.return) {
      const selectedDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(selectedDay).padStart(2, '0')}`;
      const dayEvents = events.filter(e => e.start.startsWith(selectedDate));
      onUpdate?.({ selectedDate, selectedEvent: dayEvents[0] });
    }
  });

  const getEventsForDay = (day: number): Event[] => {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    return events.filter(e => e.start.startsWith(dateStr));
  };

  const renderWeek = (startIdx: number): React.ReactNode => {
    const cells = [];
    for (let i = 0; i < 7; i++) {
      const dayNum = startIdx + i - firstDay + 1;
      if (dayNum < 1 || dayNum > daysInMonth) {
        cells.push(<Box key={i} width={5}><Text color="gray">    </Text></Box>);
      } else {
        const isSelected = dayNum === selectedDay;
        const isToday = dayNum === today.getDate() && month === today.getMonth() && year === today.getFullYear();
        const dayEvents = getEventsForDay(dayNum);
        const hasEvents = dayEvents.length > 0;

        cells.push(
          <Box key={i} width={5}>
            <Text
              color={isSelected ? 'black' : isToday ? 'cyan' : hasEvents ? 'yellow' : 'white'}
              backgroundColor={isSelected ? 'cyan' : undefined}
              bold={isToday}
            >
              {String(dayNum).padStart(3, ' ')}{hasEvents ? '*' : ' '}
            </Text>
          </Box>
        );
      }
    }
    return <Box>{cells}</Box>;
  };

  const selectedDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(selectedDay).padStart(2, '0')}`;
  const selectedEvents = getEventsForDay(selectedDay);

  return (
    <Box flexDirection="column" borderStyle="round" borderColor="cyan" padding={1}>
      <Box marginBottom={1} justifyContent="space-between">
        <Text bold color="cyan"> {MONTHS[month]} {year} </Text>
        <Text color="gray">[/]: prev/next month | arrows: navigate | Enter: select</Text>
      </Box>

      {/* Day headers */}
      <Box>
        {DAYS.map(d => (
          <Box key={d} width={5}>
            <Text color="gray" bold>{d.padStart(4, ' ')}</Text>
          </Box>
        ))}
      </Box>

      {/* Calendar grid */}
      {[0, 7, 14, 21, 28, 35].map(startIdx => renderWeek(startIdx))}

      {/* Events for selected day */}
      <Box marginTop={1} flexDirection="column" borderStyle="single" borderColor="gray" padding={1}>
        <Text bold color="yellow">Events for {selectedDate}:</Text>
        {selectedEvents.length === 0 ? (
          <Text color="gray" dimColor>No events</Text>
        ) : (
          selectedEvents.map(e => (
            <Box key={e.id}>
              <Text color={e.color || 'white'}> {e.start.slice(11, 16) || '     '} {e.title}</Text>
            </Box>
          ))
        )}
      </Box>
    </Box>
  );
};

export default CalendarCanvas;
