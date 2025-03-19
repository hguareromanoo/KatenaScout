/**
 * API service exports - Convenience re-exports for all API services
 */

// Direct import of services
import chatService from './chatService';
import playerService from './playerService';
import appService from './appService';
import { fetchAPI } from './api';

// Named exports for destructuring imports
export {
  fetchAPI,
  chatService, 
  playerService, 
  appService
};

// Default export as an object with all services
export default {
  fetch: fetchAPI,
  chat: chatService,
  player: playerService,
  app: appService
};