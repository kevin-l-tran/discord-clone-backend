<template>
  <div class="p-6 bg-neutral-100 min-h-screen">
    <h1 class="text-3xl font-extrabold mb-6">Dashboard</h1>
    <div class="flex flex-wrap gap-6">
      <div
        v-for="group in groups"
        :key="group.id"
        @click="goToGroup(group.id)"
        class="w-64 bg-white shadow-lg rounded-xl overflow-hidden cursor-pointer transition hover:shadow-xl"
      >
        <img
          :src="group.image"
          alt="Group"
          class="w-full h-40 object-cover"
        />
        <div class="p-4">
          <h2 class="text-lg font-semibold text-gray-800">
            {{ group.name }}
          </h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const groups = [
  {
    id: 'advising',
    name: 'NSM College Advising',
    image: '/images/advising.png',
  },
  {
    id: 'cpsc449',
    name: 'Summer 2025 CPSC 449',
    image: '/images/cpsc449.png',
  },
  // More groups can be added here
]

const goToGroup = (id) => {
  router.push(`/group/${id}`)
}
</script>
