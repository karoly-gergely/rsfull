<template>
  <div class="home">
    <ProductGrid />
  </div>
</template>

<script>
import ProductGrid from '@/components/ProductGrid.vue'

export default {
  name: 'Home',
  components: {
    ProductGrid,
  },

  props: {},
  data() {
    return {}
  },
  async created() {},
}
</script>
