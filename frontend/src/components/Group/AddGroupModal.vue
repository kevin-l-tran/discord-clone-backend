<script setup lang="ts">
</script>

<template>
    <Transition enter-from-class="opacity-0 scale-75" enter-to-class="opacity-100 scale-100"
        enter-active-class="transition duration-200" leave-from-class="opacity-100" leave-to-class="opacity-0"
        leave-active-class="transition duration-200 ">
        <!-- backdrop -->
        <div class="fixed inset-0 flex items-center justify-center z-50" @click="$emit('close')">
            <!-- modal box -->
            <div class="relative bg-white rounded-3xl overflow-hidden shadow-xl" @click.stop>
                <form class="w-full max-w-xl mx-auto bg-white p-16 rounded-lg shadow space-y-4">
                    <h2 class="text-4xl font-semibold text-gray-800 text-center mb-5">Add a Group</h2>

                    <!-- Group Name -->
                    <div>
                        <input type="text" placeholder="Group Id"
                            class="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400" />
                    </div>

                    <!-- Submit -->
                    <button type="submit"
                        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded-lg transition text-lg">
                        Add Group
                    </button>
                </form>
            </div>
        </div>
    </Transition>
</template>