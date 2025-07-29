<script setup lang="ts">
import GroupCard from './components/Group/GroupCard.vue';
import CreateGroupModal from './components/Group/CreateGroupModal.vue';
import AddGroupModal from './components/Group/AddGroupModal.vue';

import { onMounted, ref } from 'vue';
import { BACKEND_URL } from './config';

const showCreate = ref(false);
const showAdd = ref(false);

const groups = ref<any[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

onMounted(async () => {
  const token = localStorage.getItem('access_token');
  try {
    const res = await fetch(BACKEND_URL + '/user-groups', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    groups.value = await res.json();
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
});
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
      <GroupCard v-for="group in groups" :key="group.id" :group-image="group.img_url" :group-name="group.name" :group-description="group.description">
      </GroupCard>

      <div
        class="w-80 bg-white shadow-lg rounded-xl border-3 border-white flex justify-evenly overflow-hidden transition duration-500 hover:shadow-xl hover:border-sky-300 flex flex-col items-center justify-between">
        <button class="text-5xl font-semibold text-gray-800 hover:text-sky-600 transition cursor-pointer p-10" @click="showAdd = true">
          + Add
        </button>
        <div class="w-64 h-1 bg-gray-300" />
        <button class="text-5xl font-semibold text-gray-800 hover:text-sky-600 transition cursor-pointer p-10" @click="showCreate = true">
          + Create
        </button>
      </div>
    </div>
  </div>

  <Teleport to="body">
    <CreateGroupModal v-show="showCreate" @close="showCreate = false"></CreateGroupModal>
  </Teleport>
  <Teleport to="body">
    <AddGroupModal v-show="showAdd" @close="showAdd = false"></AddGroupModal>
  </Teleport>
</template>
