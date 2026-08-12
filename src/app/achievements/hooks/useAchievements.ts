/**
 * useAchievements - Achievement filtering, stats, and tab state
 */

'use client';

import { useState } from 'react';
import mockAchievements from '../achievements.json';

export type AchievementTab = 'all' | 'unlocked' | 'locked';

/**
 * Declared rather than derived from achievements.json. `typeof json[0] &
 * { unlockedAt?: string }` looks equivalent, but TypeScript infers the array as
 * a union of "has unlockedAt" and "has unlockedAt?: undefined" element shapes,
 * and intersecting the latter narrows the property to never - so locked
 * achievements stopped being assignable to their own type.
 */
export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  points: number;
  unlocked: boolean;
  progress: number;
  maxProgress: number;
  category: string;
  unlockedAt?: string;
}

export function useAchievements() {
  const [selectedTab, setSelectedTab] =
    useState<AchievementTab>('all');

  const totalPoints = mockAchievements
    .filter((a) => a.unlocked)
    .reduce((sum, a) => sum + a.points, 0);

  const totalPossiblePoints = mockAchievements.reduce(
    (sum, a) => sum + a.points,
    0
  );

  const level = Math.floor(totalPoints / 500) + 1;
  const pointsToNextLevel = level * 500 - totalPoints;

  const filteredAchievements = mockAchievements.filter((a) => {
    if (selectedTab === 'unlocked') return a.unlocked;
    if (selectedTab === 'locked') return !a.unlocked;
    return true;
  });

  const recentUnlocked = mockAchievements
    .filter((a) => a.unlocked && a.unlockedAt)
    .sort(
      (a, b) =>
        new Date(b.unlockedAt!).getTime() -
        new Date(a.unlockedAt!).getTime()
    )
    .slice(0, 5);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffDays = Math.floor(
      (now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24)
    );
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    return date.toLocaleDateString();
  };

  const unlockedCount = mockAchievements.filter(
    (a) => a.unlocked
  ).length;

  return {
    selectedTab,
    setSelectedTab,
    totalPoints,
    totalPossiblePoints,
    level,
    pointsToNextLevel,
    filteredAchievements,
    recentUnlocked,
    formatDate,
    unlockedCount,
    totalCount: mockAchievements.length,
  };
}
