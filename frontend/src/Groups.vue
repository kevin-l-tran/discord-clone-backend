<script setup lang="ts">
import GroupCard from './components/Group/GroupCard.vue';

const tempGroups = [
  {
    id: 'advising',
    name: 'NSM College Advising',
    image: '/src/assets/background.avif',
    description: 'test description'
  },
  {
    id: 'cpsc449',
    name: 'Summer 2025 CPSC 449 ijerokgljdrikogdioguduiogjuigjrdiujgiujj',
    image: '/src/assets/background.avif',
    description: 'Gg,0N]pa/y$a +F%.zHHHBj hZ3u+.vB [R2jJ& i #BQ6y=7d #qP9ct fA 8V} P} 4M:Swu( wPnw dyZ0J]0;dgT ;8aEpR( DHd=G=w% m%x8aK N/QN+&n .d7NQeB SKcB}j[e}Xq#L&r&ww#kzj)yxj%89rge6Tk'
  },
];
</script>

<template>
  <div class="p-6 bg-neutral-100 min-h-screen relative">
    <div className="fixed inset-0 pointer-events-none">
      <svg width="100%" height="100%">
        <defs>
          <pattern id="dots" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
            <circle cx="2" cy="2" r="2" fill="#bae6fd" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#dots)" />
      </svg>
    </div>

    <header class="m-8 relative z-10">
      <h1 class="text-6xl text-blue-950 font-black mb-6 pb-3 border-b-4 border-sky-500">Your Groups</h1>
    </header>

    <div class="flex flex-wrap gap-10 m-8 relative z-10">
      <GroupCard v-for="group in tempGroups" :key="group.id" :group-image="group.image" :group-name="group.name" :group-description="group.description">
      </GroupCard>

      <div
        class="w-80 bg-white shadow-lg rounded-xl border-3 border-white flex justify-evenly overflow-hidden transition duration-500 hover:shadow-xl hover:border-sky-300 flex flex-col items-center justify-between">
        <button class="text-5xl font-semibold text-gray-800 hover:text-sky-600 transition cursor-pointer p-10">
          + Add
        </button>
        <div class="w-64 h-1 bg-gray-300" />
        <button class="text-5xl font-semibold text-gray-800 hover:text-sky-600 transition cursor-pointer p-10">
          + Create
        </button>
      </div>
    </div>
  </div>


</template>
