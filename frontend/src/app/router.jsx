import React from 'react';
import { createBrowserRouter } from 'react-router-dom';
import PublicLayout from '../components/layout/PublicLayout';
import AdminLayout from '../components/layout/AdminLayout';
import HomeView from '../components/views/HomeView';
import MapView from '../components/views/MapView';
import ExploreView from '../components/views/ExploreView';
import AdminView from '../components/views/AdminView';
import NotFoundView from '../components/views/NotFoundView';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <PublicLayout />,
    children: [
      {
        index: true,
        element: <HomeView />,
      },
      {
        path: 'map',
        element: <MapView />,
      },
      {
        path: 'explore',
        element: <ExploreView />,
      },
    ],
  },
  {
    path: '/admin',
    element: <AdminLayout />,
    children: [
      {
        index: true,
        element: <AdminView />,
      },
    ],
  },
  {
    path: '*',
    element: <NotFoundView />,
  },
]);

