# coding=utf-8
# import...


class PublicationListView(ListView):
    model = Publication
    template = 'publications/list.html'

    def get_paginate_by(self, queryset):
        return COUNTS.get(self.request._cookies['obj_per_page'], 5)
    
    def get_queryset(self):
        return self.model.objects.select_related().filter(status=1)

    def get_context_data(self, **kwargs)
        context = super(PublicationListView, self).get_context_data(**kwargs)
        context['page_title'] = u'Some Page'
        return context

def document_to_response(request,slug=None):
    if slug:
        try:
            doc = Document.objects.get(slug=slug)
            doc_template = Template(doc.template.text)
            print  doc_template.render(Context(dict(doc.variable_set.all().values_list('name','value')))),
            response = HttpResponse(
                doc_template.render(Context(dict(doc.variable_set.all().values_list('name','value')))),
                mimetype='application/vnd.ms-word'
            )
            response.__setitem__('Content-Disposition','attachment;Filename=%s.doc' % doc.name)
            return response

        except Exception,e:
            print e
            return Http404()
    else:
        return Http404()
