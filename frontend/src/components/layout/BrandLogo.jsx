import React from 'react';

// Original project identity: a botanical leaf and an elephant wearing headphones.
export default function BrandLogo() {
  return <svg className="brand-logo" viewBox="0 0 190 60" fill="none" aria-hidden="true" focusable="false">
    <rect x="1" y="3" width="54" height="54" rx="18" fill="currentColor" />
    <path d="M17 35v-8a12 12 0 0 1 24 0v8" stroke="#f4dd9b" strokeWidth="3" strokeLinecap="round" />
    <path d="M22 27c0-5 13-6 14 1v12c0 5 8 5 8-1" stroke="#fffdf5" strokeWidth="4" strokeLinecap="round" />
    <path d="M23 28c-10-3-11 13-2 13 4 0 6-5 5-9" fill="#fffdf5" />
    <circle cx="32" cy="28" r="1.4" fill="#f4dd9b" />
    <path d="M30 16c-1-8 7-10 12-9-1 7-6 11-12 9Z" fill="#b6d49a" />
    <path d="m31 15 7-5" stroke="#1c5139" strokeWidth="1.2" strokeLinecap="round" />
    <text x="66" y="30" fill="currentColor" fontFamily="'Zoo Sans', sans-serif" fontSize="21" fontWeight="800" letterSpacing="1">TCV</text>
    <path d="M121 16v15" stroke="currentColor" strokeOpacity=".25" />
    <text x="130" y="21" fill="currentColor" fontFamily="'Zoo Sans', sans-serif" fontSize="8" fontWeight="700" letterSpacing="1">SAIGON</text>
    <text x="130" y="32" fill="currentColor" fontFamily="'Zoo Sans', sans-serif" fontSize="10" fontWeight="700" letterSpacing="2">ZOO</text>
    <text x="66" y="46" fill="currentColor" fontFamily="'Zoo Sans', sans-serif" fontSize="7.5" fontWeight="500" letterSpacing="1.7">AUDIO GUIDE</text>
  </svg>;
}
