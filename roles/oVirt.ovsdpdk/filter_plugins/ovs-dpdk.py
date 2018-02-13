#!/usr/bin/python


class FilterModule(object):
    def filters(self):
        return {
            'get_core_mask': self.get_core_mask,
            'get_pmd_cores': self.get_pmd_cores,
        }

    def _range_to_list(self, core_list):
        edges = core_list.rstrip().split('-')
        return list(range(int(edges[0]), int(edges[1]) + 1))

    def _list_from_string(self, str_list):
        return list(map(int, str_list.rstrip().split(',')))

    def get_core_mask(self, cores):
        mask = 0
        for core in cores:
            mask |= (1 << int(core))
        return hex(mask)

    def get_pmd_cores(self, nics_numa_info, pmd_threads_count):
        pmd_cores = []
        for node_info in nics_numa_info.values():
            nics_count = node_info['nics']
            cores = node_info['cpu_list']
            if '-' in cores:
                cores = self._range_to_list(cores)
            if ',' in cores:
                self._list_from_string(cores
                                       )
            num_cores = nics_count * pmd_threads_count
            while num_cores > 0:
                min_core = min(cores)
                pmd_cores.append(min_core)
                cores.remove(min_core)
                num_cores -= 1

        return pmd_cores
