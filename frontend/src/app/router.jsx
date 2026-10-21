import React, { lazy, Suspense } from 'react';
import { createBrowserRouter } from 'react-router-dom';
import PublicLayout from '../components/layout/PublicLayout';
import AdminLayout from '../components/layout/AdminLayout';
import HomeView from '../components/views/HomeView';
import MapView from '../components/views/MapView';
import ExploreView from '../components/views/ExploreView';
import ItineraryView from '../components/views/ItineraryView';
import GuideView from '../components/views/GuideView';
import NotFoundView from '../components/views/NotFoundView';

const AdminView = lazy(() => import('../components/views/AdminView'));
const AnalyticsDashboard = lazy(() => import('../components/views/AnalyticsDashboard'));

export const router = createBrowserRouter([
  {
    path: '/',
    element: <PublicLayout />,
    children: [
      { index: true, element: <HomeView /> },
      { path: 'map', element: <MapView /> },
      { path: 'explore', element: <ExploreView /> },
      { path: 'itinerary', element: <ItineraryView /> },
      { path: 'guide', element: <GuideView /> },
    ],
  },
  {
    path: '/admin',
    element: <AdminLayout />,
    children: [
      { index: true, element: <Suspense fallback={<div className="card">Loading admin…</div>}><AdminView /></Suspense> },
      { path: 'analytics', element: <Suspense fallback={<div className="card">Loading dashboard…</div>}><AnalyticsDashboard /></Suspense> },
    ],
  },
  { path: '*', element: <NotFoundView /> },
]);
