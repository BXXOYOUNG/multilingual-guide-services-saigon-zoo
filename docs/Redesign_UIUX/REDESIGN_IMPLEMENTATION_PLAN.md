# TCV WEBSITE – UI/UX REDESIGN IMPLEMENTATION PLAN

**Project:** TCV – Saigon Zoo Audio Guide  
**Redesign Direction:** Hybrid Scrolling + Sticky Storytelling  
**Scope:** Frontend UI/UX Redesign  
**Priority:** Preserve Existing Functionality  
**Development Approach:** Audit-First, Incremental Implementation

---

# 1. PROJECT OBJECTIVE

## 1.1. Main Objective

Redesign the existing TCV website to provide a modern, immersive, continuous scrolling experience.

The new UX should allow users to discover the website's existing features by scrolling vertically through a sequence of well-organized sections instead of navigating between multiple pages to discover each feature.

The design direction combines:

- Hybrid Scrolling Experience.
- Sticky Storytelling.
- Scroll-triggered Animations.
- Section-based Navigation.
- Responsive Design.
- Consistent Visual Design System.

The redesigned website must preserve all existing backend functionality and business behavior.

## 1.2. Core Design Philosophy

Transform the website from:

A multi-page, navigation-oriented experience where users must actively select individual features.

Into:

A continuous, vertically guided experience where users progressively discover existing features through scrolling.

However, direct navigation must remain available for users who already know which feature they want to access.

## 1.3. Non-negotiable Constraints

The following constraints apply throughout the entire project.

### Backend Protection

DO NOT modify:

- Backend source code.
- Backend business logic.
- API endpoints.
- API request/response contracts.
- Database schemas.
- Database models.
- Authentication and authorization logic.
- Audio processing logic.
- GPS and geolocation logic.
- Map processing logic.
- Route generation logic.
- Offline download and caching logic.

### Functional Protection

All existing functionality must continue working exactly as before.

Do not replace existing functional implementations with mock data, hardcoded data, temporary UI simulations, or newly invented business logic.

### Frontend Scope

Allowed changes:

- Page layout and composition.
- Component presentation.
- Component organization when approved.
- CSS and styling.
- Typography and color system.
- Navigation presentation.
- Scroll interactions.
- Animation and transitions.
- Responsive behavior.
- Frontend-only UI state and presentation logic.

If a proposed change requires modifying backend behavior or API contracts, STOP and report the dependency. Do not implement the change.

---

# 2. TARGET UX ARCHITECTURE

The new homepage should follow this proposed section order.

The agent must audit the existing implementation and map each existing feature to the appropriate section before making changes.

## Section 01 – Hero / Welcome

Purpose:
Introduce the TCV Audio Guide and encourage users to begin exploring.

Content:

- Main headline.
- Short introduction.
- Hero wildlife photography.
- Primary CTA: Explore the map.
- Secondary CTA: Explore suggested routes.
- Scroll indicator.

Interaction:

- Smooth scroll to the next section.
- Subtle image animation.
- Text reveal animation.

Keep the existing brand identity and visual direction.

## Section 02 – Animal Discovery

Purpose:
Allow visitors to discover animals before or during their visit.

Content:

- Featured animals.
- Animal images.
- Animal names.
- Short descriptions.
- Existing animal information.

Design direction:

- Use editorial-style animal cards.
- Consider larger image layouts.
- Use sticky storytelling for featured animals where appropriate.
- Reveal content progressively as users scroll.

Interaction:

- Existing animal selection behavior must remain intact.
- Existing links to animal details must remain functional.
- Do not invent animal information.

## Section 03 – Audio Experience

Purpose:
Introduce the existing audio guide usage modes.

Content:

1. Listen directly on the website.
2. Automatic playback based on location.
3. Download audio for offline listening.

Design direction:

- Present the three modes as one coherent experience.
- Use a combination of visual explanation, icons, and interactive cards.
- Avoid presenting them as unrelated navigation destinations.

Interaction:

- Reuse existing audio functionality.
- Preserve playback behavior.
- Preserve existing audio controls.
- Preserve offline download behavior.
- Do not rewrite audio services or hooks.

## Section 04 – Interactive Map

Purpose:
Introduce the existing interactive map within the scrolling experience.

Content:

- Map preview or embedded map.
- Existing animal locations.
- Existing visitor location functionality.
- Existing map controls.

Design direction:

- Allocate sufficient viewport space for map interaction.
- Avoid placing excessive text around the map.
- Use sticky layout only if it does not interfere with map controls.

Interaction:

- Preserve existing map implementation.
- Preserve GPS and location permissions.
- Preserve marker selection.
- Preserve map interactions.
- Preserve existing navigation behavior where necessary.

Important:
Do not recreate the map using a static image or mock interface.

## Section 05 – Suggested Routes

Purpose:
Help visitors select an appropriate sightseeing route.

Content:

- Existing suggested routes.
- Route descriptions.
- Existing estimated duration.
- Existing number of stops.
- Existing route details.

Design direction:

- Use large route cards.
- Make route differences easy to understand.
- Present the routes as a natural continuation of the map section.

Interaction:

- Preserve existing route selection behavior.
- Preserve route data.
- Preserve route generation and calculation logic.
- Preserve existing navigation to route details if applicable.

## Section 06 – Offline Audio Preparation

Purpose:
Help visitors prepare audio content before visiting the zoo.

Content:

- Existing QR codes.
- Supported languages.
- Existing download instructions.
- Offline usage instructions.

Design direction:

- Present QR codes clearly.
- Group languages consistently.
- Use a clean preparation-oriented layout.

Interaction:

- Preserve existing QR destinations.
- Preserve download functionality.
- Preserve language selection.
- Do not generate replacement QR codes without verifying their destinations.

## Section 07 – Getting Started

Purpose:
Provide a final introduction to using the TCV Audio Guide.

Content:

- Basic usage instructions.
- Important notes.
- Existing help information.
- CTA to start exploring.

Design direction:

- Keep the section concise.
- Avoid repeating information already explained.
- Finish with a clear call to action.

## Footer

Preserve existing footer information and links.

The footer may be visually redesigned but must not lose existing navigation destinations or important information.

---

# 3. IMPLEMENTATION WORKFLOW

The project must be executed in the following phases.

Do not skip phases or combine them without approval.

# PHASE 0 – PROJECT BASELINE AND SAFETY

Objective:
Establish the current state of the project before making any modifications.

Tasks:

1. Inspect the repository structure.
2. Identify the frontend and backend directories.
3. Identify the current Git branch.
4. Inspect existing uncommitted changes.
5. Identify the current build and development commands.
6. Identify the existing test commands.
7. Confirm how frontend and backend communicate.
8. Establish a baseline of the current application.

Required deliverables:

- Repository structure summary.
- Frontend/backend boundary identification.
- Existing Git status.
- Build and test commands.
- List of known existing functional flows.

Rules:

- Do not modify any source code.
- Do not delete existing files.
- Do not reset or overwrite existing user changes.
- Do not create a new architecture.

Checkpoint:

Report the findings before proceeding.

# PHASE 1 – FRONTEND ARCHITECTURE AUDIT

Objective:
Understand the existing frontend architecture and identify which components can be reused.

## 1.1. Page and Route Audit

Inspect:

- All existing frontend routes.
- Homepage.
- Map page.
- Audio page.
- Suggested routes page.
- Guide/help page.
- Animal detail pages or related pages.

For each route, document:

- Route path.
- Main purpose.
- Components used.
- Functional dependencies.
- API dependencies.
- Navigation relationships.

## 1.2. Component Audit

Classify existing components into:

A. Presentation Components

Examples:

- Buttons.
- Cards.
- Headers.
- Footers.
- Typography components.
- Layout wrappers.

B. Functional Components

Examples:

- Audio player.
- Interactive map.
- GPS controls.
- Route selectors.
- QR download components.

C. Mixed Components

Components containing both UI presentation and functional/business-related behavior.

For each component, identify whether it can be reused directly, restyled, wrapped, or requires a carefully controlled frontend refactor.

## 1.3. API and Service Dependency Audit

Inspect how frontend components interact with:

- API services.
- Custom hooks.
- State management.
- Authentication.
- Audio services.
- Map services.
- Location services.
- Offline storage.

Create a dependency map.

Example:

Homepage
  -> MapSection
      -> ExistingMapComponent
          -> ExistingMapHook
              -> ExistingMapService
                  -> Existing API

This is an illustrative dependency structure, not an instruction to change the current architecture.

## 1.4. Functional Behavior Inventory

Create an inventory of all existing functionality.

For each feature, document:

- Current user flow.
- Entry point.
- Required inputs.
- Expected outputs.
- Existing frontend state.
- Existing API calls.
- Existing error handling.
- Existing loading states.
- Existing permission requirements.

## 1.5. Reuse and Risk Assessment

Classify each existing component:

- REUSE: Reuse without changing functional behavior.
- RESTYLE: Modify visual presentation only.
- WRAP: Place inside a new layout or section.
- REFACTOR: Requires frontend restructuring and explicit approval.
- PROTECT: Must not be modified because it contains sensitive functional logic.

Required deliverables:

1. Frontend Architecture Audit.
2. Route Inventory.
3. Component Inventory.
4. API Dependency Map.
5. Functional Behavior Inventory.
6. Reuse and Risk Assessment.

Checkpoint:

Submit the audit and wait for approval.

No implementation is allowed in this phase.

# PHASE 2 – UX ARCHITECTURE AND USER FLOW

Objective:
Define how existing features will be reorganized into the new scrolling experience.

## 2.1. Information Architecture

Map all existing pages and features into the seven proposed sections.

For each section, define:

- Purpose.
- User intent.
- Content.
- Existing components to reuse.
- Entry and exit interactions.
- Navigation destinations.

## 2.2. User Flow Design

Define the primary visitor journey:

Homepage
  -> Discover Animals
  -> Learn About Audio
  -> Explore Map
  -> Select Suggested Route
  -> Prepare Offline Audio
  -> Start Visit

This is the primary guided journey.

Also preserve alternative journeys for users who want to:

- Open the map immediately.
- Start listening immediately.
- Download audio immediately.
- Open a suggested route directly.
- Navigate to an existing page through a direct URL.

Do not force all users to follow the same sequence.

## 2.3. Navigation Design

Design a simplified sticky header.

Requirements:

- Preserve the TCV logo and brand identity.
- Provide access to important existing destinations.
- Show the current section or active navigation state.
- Support smooth scrolling to sections.
- Preserve direct access to existing pages where applicable.
- Provide an appropriate mobile navigation layout.

## 2.4. Wireframe

Create a low-fidelity wireframe for:

- Desktop.
- Tablet.
- Mobile.

The wireframe must define:

- Section order.
- Section boundaries.
- Content hierarchy.
- Image placement.
- CTA placement.
- Navigation behavior.
- Sticky elements.
- Scrolling behavior.

Required deliverables:

1. Information Architecture.
2. User Flow Diagram.
3. Navigation Specification.
4. Desktop Wireframe.
5. Mobile Wireframe.
6. Section-to-Existing-Component Mapping.

Checkpoint:

Wait for approval before visual implementation.

# PHASE 3 – VISUAL DESIGN SYSTEM

Objective:
Establish consistent visual rules before implementing the redesign.

## 3.1. Brand Preservation

Retain the current TCV identity:

- Forest green.
- Warm cream.
- Natural photography.
- Botanical visual direction.
- Rounded card language.
- Clean editorial typography.

The design should feel like a professional nature-oriented digital experience.

Do not arbitrarily replace the existing brand identity.

## 3.2. Design Tokens

Audit and define reusable tokens for:

- Primary colors.
- Secondary colors.
- Background colors.
- Text colors.
- Border colors.
- Typography scale.
- Font weights.
- Spacing scale.
- Border radius.
- Shadows.
- Container widths.
- Breakpoints.
- Animation durations.

Reuse existing design tokens where possible.

Avoid introducing duplicated or conflicting styling systems.

## 3.3. Component Design

Define consistent visual specifications for:

- Buttons.
- Navigation.
- Section headings.
- Cards.
- Image containers.
- Audio controls.
- Route cards.
- Language selectors.
- QR containers.
- Progress indicators.

Do not recreate existing functional components when restyling or wrapping them is sufficient.

Required deliverables:

1. Design Token Specification.
2. Component Styling Specification.
3. Typography Hierarchy.
4. Responsive Breakpoint Specification.

Checkpoint:

Obtain approval of the visual direction before implementation.

# PHASE 4 – FRONTEND UI IMPLEMENTATION

Objective:
Implement the approved UI/UX design while preserving all existing functional behavior.

## 4.1. Implementation Rules

- Work incrementally.
- Implement one section at a time.
- Reuse existing components.
- Reuse existing hooks and services.
- Preserve existing API integration.
- Preserve existing state management.
- Preserve loading, error, and empty states.
- Do not replace real functionality with mock functionality.
- Do not modify backend files.

If a functional component must be moved, preserve its props, state dependencies, event handlers, and lifecycle behavior.

## 4.2. Implementation Order

Implement in this order:

1. Global layout and design tokens.
2. Sticky header.
3. Scroll progress navigation.
4. Hero section.
5. Animal discovery section.
6. Audio experience section.
7. Interactive map section.
8. Suggested routes section.
9. Offline audio section.
10. Getting started section.
11. Footer.
12. Responsive adjustments.

After each section:

- Build the application.
- Check browser console errors.
- Verify the section visually.
- Verify existing functionality.
- Inspect unintended changes.

Do not implement all sections simultaneously without intermediate verification.

## 4.3. Existing Page Compatibility

The new homepage must not make existing routes inaccessible.

If an existing page is integrated into the homepage:

- Reuse the existing component where feasible.
- Preserve direct route access.
- Preserve existing navigation behavior.
- Avoid creating duplicated implementations of the same feature.

A component may have a new presentation wrapper, but its functional contract must remain intact.

# PHASE 5 – SCROLL INTERACTION AND ANIMATION

Objective:
Implement the Hybrid Scrolling and Sticky Storytelling experience.

## 5.1. Scroll-triggered Reveal

Use viewport-based triggering to animate content when it enters the viewport.

Suitable effects:

- Fade in.
- Subtle slide up.
- Image scale.
- Staggered card appearance.

Requirements:

- Avoid excessive animation.
- Avoid repeated animation that distracts users.
- Ensure content remains accessible if animation fails.
- Avoid hiding important content until JavaScript runs.

## 5.2. Sticky Storytelling

Use sticky layouts for sections where they improve storytelling.

Recommended sections:

- Animal Discovery.
- Audio Experience.
- Suggested Routes.

Requirements:

- Sticky elements must not cover important content.
- Sticky sections must not prevent normal scrolling.
- Content must remain accessible on mobile.
- Avoid nested sticky elements unless necessary.

## 5.3. Scroll Progress

Implement a progress indicator that reflects the current section.

Requirements:

- Active section detection.
- Accurate progress updates.
- Navigation to sections when selected.
- Proper handling of header offsets.
- No conflict with existing routes.

Use Intersection Observer or an equivalent frontend mechanism where appropriate.

## 5.4. Scroll Snap

Scroll snap is optional.

Do not apply mandatory full-page snapping to the entire website.

Use natural scrolling as the default.

Only introduce snap behavior when the content structure and usability justify it.

## 5.5. Accessibility

Support:

- Keyboard navigation.
- Visible focus states.
- Reduced motion preferences.
- Sufficient color contrast.
- Appropriate semantic HTML.
- Screen-reader-friendly controls.

# PHASE 6 – RESPONSIVE DESIGN

Objective:
Ensure the redesigned experience works across screen sizes.

Test at minimum:

Desktop:
- 1440px width.
- 1280px width.

Tablet:
- 768px width.

Mobile:
- 390px width.
- 360px width.

These are test viewport sizes, not mandatory CSS breakpoints.

Requirements:

- No horizontal overflow.
- No clipped text.
- No overlapping controls.
- Appropriate image ratios.
- Responsive navigation.
- Touch-friendly buttons.
- Functional map controls.
- Functional audio controls.
- Sticky behavior must remain usable.
- Cards must adapt to available width.

Do not simply shrink desktop layouts to fit mobile.

Design the mobile experience intentionally.

# PHASE 7 – REGRESSION TESTING

Objective:
Verify that the redesign has not broken existing functionality.

The agent must compare the original functional inventory from Phase 1 against the redesigned implementation.

## 7.1. Functional Regression Checklist

### General

- [ ] Homepage loads correctly.
- [ ] Existing routes remain accessible.
- [ ] Header navigation works.
- [ ] All existing links work.
- [ ] No unexpected redirects.

### Animal Discovery

- [ ] Animal information loads correctly.
- [ ] Animal selection works.
- [ ] Existing detail links work.

### Audio

- [ ] Audio playback works.
- [ ] Play/pause works.
- [ ] Audio selection works.
- [ ] Language selection works.
- [ ] Existing audio controls work.

### Map and GPS

- [ ] Map loads correctly.
- [ ] Markers are displayed correctly.
- [ ] Marker selection works.
- [ ] Location permissions work.
- [ ] GPS behavior remains unchanged.

### Suggested Routes

- [ ] Existing route data loads.
- [ ] Route selection works.
- [ ] Route details work.
- [ ] Existing route calculations remain unchanged.

### Offline Audio

- [ ] QR codes lead to the correct destinations.
- [ ] Audio downloads work.
- [ ] Offline functionality works.
- [ ] Language selection remains functional.

### Responsive

- [ ] Desktop layout works.
- [ ] Tablet layout works.
- [ ] Mobile layout works.
- [ ] No horizontal overflow.
- [ ] No inaccessible controls.

## 7.2. Technical Verification

Check:

- Frontend build success.
- Existing automated tests.
- Browser console errors.
- Network request failures.
- API request/response compatibility.
- Missing assets.
- Unexpected frontend exceptions.

Do not claim a test passed if it was not executed.

If a test cannot be performed, report the reason and mark it as NOT VERIFIED.

# PHASE 8 – FINAL AUDIT AND DELIVERY

Objective:
Confirm the project satisfies all redesign requirements.

Required checks:

1. Compare modified files against the original Git baseline.
2. Confirm no backend files were modified.
3. Confirm no API contracts were modified.
4. Confirm no database changes were introduced.
5. Confirm all existing functional flows pass regression testing.
6. Confirm responsive behavior.
7. Confirm scroll interactions.
8. Confirm no new critical console errors.

Required deliverables:

- Final implementation summary.
- List of modified files.
- List of reused components.
- List of new components.
- Regression test results.
- Known issues.
- Unverified functionality.
- Backend/API preservation confirmation.
- Screenshots of the redesigned desktop and mobile interfaces.

Do not automatically commit, push, or deploy changes unless explicitly requested.

---

# 4. CHANGE CONTROL PROTOCOL

Any modification outside the approved scope requires explicit approval.

Examples:

| Proposed Change | Permission |
|---|---|
| Change CSS | Allowed |
| Change section layout | Allowed after UX approval |
| Add scroll animation | Allowed |
| Create a presentation wrapper | Allowed |
| Move an existing frontend component | Requires impact analysis and approval |
| Change frontend API request structure | Not allowed |
| Change API endpoint | Not allowed |
| Change backend business logic | Not allowed |
| Change database schema | Not allowed |
| Rewrite audio functionality | Not allowed |
| Replace real API data with mock data | Not allowed |

If the agent discovers a conflict:

1. Stop the affected implementation.
2. Explain the conflict.
3. Identify the affected files and dependencies.
4. Propose a frontend-only solution.
5. Wait for approval.

Do not silently expand project scope.

---

# 5. AGENT WORKING RULES

These rules apply to every implementation task.

## Rule 1 – Audit Before Modification

Inspect existing code before changing it.

Never assume the existing architecture based on filenames alone.

## Rule 2 – Preserve Existing Behavior

A visual redesign must not change the underlying functional behavior.

## Rule 3 – Minimize Unnecessary Refactoring

Do not rewrite working components simply because a new design is being introduced.

Prefer wrapping, styling, and composition over rewriting.

## Rule 4 – One Logical Task at a Time

Do not implement multiple large sections simultaneously.

Complete, test, and report each logical task before proceeding.

## Rule 5 – Report Actual Progress

After each task, report:

- What was inspected.
- What was modified.
- Why it was modified.
- Which existing components were reused.
- Which functionality was tested.
- Whether backend-related files remained unchanged.
- Any unresolved issues.

## Rule 6 – Do Not Invent Requirements

If a design decision depends on unknown functionality or unavailable information, ask for clarification instead of inventing a solution.

## Rule 7 – Protect Existing User Changes

Never overwrite unrelated changes or discard uncommitted work.

---

# 6. DEFINITION OF DONE

The redesign is considered complete only when all the following conditions are met.

### UX

- The homepage follows the approved Hybrid Scrolling Experience.
- Sections have a clear information hierarchy.
- Users can discover features through scrolling.
- Direct navigation remains available.
- Sticky Storytelling is used appropriately.
- Scroll progress works correctly.

### UI

- Visual design is consistent.
- Typography and spacing are standardized.
- Existing TCV brand identity is preserved.
- Responsive layouts work correctly.
- Animations are smooth and non-disruptive.

### Functionality

- All existing functionality remains operational.
- Existing API contracts are preserved.
- No backend logic has been modified.
- No database structure has been modified.
- No critical functional regression exists.

### Delivery

- All modifications are documented.
- All tests have recorded results.
- Unverified areas are explicitly reported.
- No unauthorized deployment or Git operation has occurred.

---

# 7. FINAL EXECUTION INSTRUCTION

Start with PHASE 0 and PHASE 1 only.

Do not modify any source code during these phases.

After completing the audit, submit the findings and wait for explicit approval before proceeding to PHASE 2.

The redesign must be implemented incrementally, with approval checkpoints between major phases.

The highest priority throughout this project is:

**PRESERVE EXISTING BACKEND AND FUNCTIONALITY. IMPROVE THE USER EXPERIENCE WITHOUT BREAKING THE SYSTEM.**